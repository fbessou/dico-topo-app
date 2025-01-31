import elasticsearch
import pprint
from flask import current_app


class SearchIndexManager(object):

    @staticmethod
    def query_index(index, query, ranges=(), groupby=None, sort_criteriae=None, page=None, per_page=None, after=None):
        if sort_criteriae is None:
            sort_criteriae = []
        if hasattr(current_app, 'elasticsearch'):
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "query_string": {
                                    "query": query,
                                    "default_operator": "AND"
                                }
                            }
                        ]
                    },
                },
                "aggregations": {

                },
                "sort": [
                    #  {"creation": {"order": "desc"}}
                    *sort_criteriae
                ]
            }

            if len(ranges) > 0:
                for range in ranges:
                    body["query"]["bool"]["must"].append({"range": range})

            if groupby is not None:
                body["aggregations"] = {
                    "items": {
                        "composite": {
                            "sources": [
                                {
                                    "item": {
                                        "terms": {
                                            "field": groupby,
                                        },
                                    }
                                },
                            ],
                            "size": per_page
                        }
                    },
                    "type_count": {
                        "cardinality": {
                            "field": "place-id"
                        }
                    }
                }
                body["size"] = 0

                sort_criteriae.reverse()
                for crit in sort_criteriae:
                    for crit_name, crit_order in crit.items():
                        body["aggregations"]["items"]["composite"]["sources"].insert(0,
                            {
                                crit_name: {
                                    "terms": {"field": crit_name, **crit_order},
                                }
                            }
                        )

                if after is not None:
                    sources_keys = [list(s.keys())[0] for s in body["aggregations"]["items"]["composite"]["sources"]]
                    body["aggregations"]["items"]["composite"]["after"] = {key: value for key, value in zip(sources_keys, after.split(','))}
                    print(sources_keys, after, {key: value for key, value in zip(sources_keys, after.split(','))})

            if per_page is not None:
                if page is None or groupby is not None:
                    page = 0
                else:
                    page = page - 1  # is it correct ?
                body["from"] = page * per_page
                body["size"] = per_page
            else:
                body["from"] = 0 * per_page
                body["size"] = per_page
                # print("WARNING: /!\ for debug purposes the query size is limited to", body["size"])
            try:
                if index is None or len(index) == 0:
                    index = current_app.config["DEFAULT_INDEX_NAME"]

                pprint.pprint(body)
                search = current_app.elasticsearch.search(index=index, body=body)
                # from elasticsearch import Elasticsearch
                # scan = Elasticsearch.helpers.scan(client=current_app.elasticsearch, index=index, body=body)

                from collections import namedtuple
                Result = namedtuple("Result", "index id type score")

                results = [Result(str(hit['_index']), str(hit['_id']), str(hit['_source']["type"]),
                                  str(hit['_score']))
                           for hit in search['hits']['hits']]

                buckets = []
                after_key = None
                count = search['hits']['total']['value']

                #print(body, len(results), search['hits']['total'], index)
                #pprint.pprint(search)
                if 'aggregations' in search:
                    buckets = search["aggregations"]["items"]["buckets"]

                    # grab the after_key returned by ES for future queries
                    if "after_key" in search["aggregations"]["items"]:
                        after_key = search["aggregations"]["items"]["after_key"]
                    print("aggregations: {0} buckets; after_key: {1}".format(len(buckets), after_key))
                    #pprint.pprint(buckets)
                    count = search["aggregations"]["type_count"]["value"]

                return results, buckets, after_key, count

            except Exception as e:
                raise e

    @staticmethod
    def add_to_index(index, id, payload):
        # print("ADD_TO_INDEX", index, id)
        current_app.elasticsearch.index(index=index, id=id, body=payload)

    @staticmethod
    def remove_from_index(index, id):
        # print("REMOVE_FROM_INDEX", index, id)
        try:
            current_app.elasticsearch.delete(index=index, id=id)
        except elasticsearch.exceptions.NotFoundError as e:
            print("WARNING: resource already removed from index:", str(e))

    # @staticmethod
    # def reindex_resources(changes):
    #    from app.api.facade_manager import JSONAPIFacadeManager
    #
    #    for target_id, target, op in changes:
    #
    #        facade = JSONAPIFacadeManager.get_facade_class(target)
    #        try:
    #            #print("try to reindex", target)
    #            if op in ('insert', 'update'):
    #                target.id = target_id
    #                f_obj = facade("", target)
    #
    #                #f_obj, kwargs, errors = facade.get_resource_facade("", id=target.id)
    #            else:
    #                target.id = target_id
    #                f_obj = facade("", target)
    #            #print("call to reindex for", target_id, target, op)
    #
    #            f_obj.reindex(op)
    #        except Exception as e:
    #            print("Error while indexing %s:" % target, e)
    #            pass
    #
