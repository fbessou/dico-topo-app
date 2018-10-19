from app.api.abstract_facade import JSONAPIAbstractFacade
from app.api.insee_ref.facade import InseeRefFacade


class CommuneFacade(JSONAPIAbstractFacade):
    """

    """
    TYPE = "commune"
    TYPE_PLURAL = "communes"

    @property
    def id(self):
        return self.obj.id

    @property
    def type(self):
        return self.TYPE

    @property
    def type_plural(self):
        return self.TYPE_PLURAL

    def get_region_resource_identifier(self):
        return None if self.obj.region is None else InseeRefFacade(self.url_prefix, self.obj.region, False, False).resource_identifier

    def get_departement_resource_identifier(self):
        return None if self.obj.departement is None else InseeRefFacade(self.url_prefix, self.obj.departement, False, False).resource_identifier

    def get_arrondissement_resource_identifier(self):
        return None if self.obj.arrondissement is None else InseeRefFacade(self.url_prefix, self.obj.arrondissement, False, False).resource_identifier

    def get_canton_resource_identifier(self):
        return None if self.obj.canton is None else InseeRefFacade(self.url_prefix, self.obj.canton, False, False).resource_identifier

    def get_region_resource(self):
        return None if self.obj.region is None else InseeRefFacade(self.url_prefix, self.obj.region,
                                                                                self.with_relationships_links,
                                                                                self.with_relationships_data).resource

    def get_departement_resource(self):
        return None if self.obj.departement is None else InseeRefFacade(self.url_prefix, self.obj.departement,
                                                                                self.with_relationships_links,
                                                                                self.with_relationships_data).resource

    def get_arrondissement_resource(self):
        return None if self.obj.arrondissement is None else InseeRefFacade(self.url_prefix, self.obj.arrondissement,
                                                                                self.with_relationships_links,
                                                                                self.with_relationships_data).resource

    def get_canton_resource(self):
        return None if self.obj.canton is None else InseeRefFacade(self.url_prefix, self.obj.canton,
                                                                                self.with_relationships_links,
                                                                                self.with_relationships_data).resource

    def get_localized_placenames_resource_identifiers(self):
        from app.api.placename.facade import PlacenameFacade
        return [] if self.obj.localized_placenames is None else [PlacenameFacade(self.url_prefix, c, False, False).resource_identifier
                                                                 for c in self.obj.localized_placenames]

    def get_localized_placenames_resource(self):
        from app.api.placename.facade import PlacenameFacade
        return [] if self.obj.localized_placenames is None else [PlacenameFacade(self.url_prefix, c,
                                                                                self.with_relationships_links,
                                                                                self.with_relationships_data).resource
                                                                 for c in self.obj.localized_placenames]

    def get_placename_resource_identifier(self):
        from app.api.placename.facade import PlacenameFacade
        return None if self.obj.placename is None else PlacenameFacade(self.url_prefix,  self.obj.placename, False, False).resource_identifier

    def get_placename_resource(self):
        from app.api.placename.facade import PlacenameFacade
        return None if self.obj.placename is None else PlacenameFacade(self.url_prefix,  self.obj.placename,
                                                                                self.with_relationships_links,
                                                                                self.with_relationships_data).resource


    @property
    def relationships(self):
        return {
            "localized-placenames": {
                "links": self._get_links(rel_name="localized-placenames"),
                "resource_identifier_getter": self.get_localized_placenames_resource_identifiers,
                "resource_getter": self.get_localized_placenames_resource
            },
            "placename": {
                "links": self._get_links(rel_name="placename"),
                "resource_identifier_getter": self.get_placename_resource_identifier,
                "resource_getter": self.get_placename_resource
            },
            "region": {
                "links": self._get_links(rel_name="region"),
                "resource_identifier_getter": self.get_region_resource_identifier,
                "resource_getter": self.get_region_resource
            },
            "departement": {
                "links": self._get_links(rel_name="departement"),
                "resource_identifier_getter": self.get_departement_resource_identifier,
                "resource_getter": self.get_departement_resource
            },
            "arrondissement": {
                "links": self._get_links(rel_name="arrondissement"),
                "resource_identifier_getter": self.get_arrondissement_resource_identifier,
                "resource_getter": self.get_arrondissement_resource
            },
            "canton": {
                "links": self._get_links(rel_name="canton"),
                "resource_identifier_getter": self.get_canton_resource_identifier,
                "resource_getter": self.get_canton_resource
            }
        }

    @property
    def resource(self):
        """ """
        res = {
            **self.resource_identifier,
            "attributes": {
                'insee-code': self.obj.id,
                'NCCENR': self.obj.NCCENR,
                'ARTMIN': self.obj.ARTMIN,
                'longlat': self.obj.longlat
            },
            "meta": self.meta,
            "links": {
                "self": self.self_link
            }
        }
        if self.with_relationships_links:
            res["relationships"] = self.get_exposed_relationships()

        return res
