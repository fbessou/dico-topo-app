import React from "react";

class PlacenameSearchForm extends React.Component {

    constructor(props) {
        super(props);

        this.handlePlacenameChange = this.handlePlacenameChange.bind(this);
        this.handleOldLabelsChange = this.handleOldLabelsChange.bind(this);
        this.handleLabelChange = this.handleLabelChange.bind(this);
        this.handleDescChange = this.handleDescChange.bind(this);
        this.handleOnKeyPress = this.handleOnKeyPress.bind(this);
        this.handleOnSearchClick = this.handleOnSearchClick.bind(this);

        if (document.getElementById("debug-mode")){
           this.api_base_url = "http://localhost:5003/dico-topo/api/1.0";
        } else {
           this.api_base_url = "/dico-topo/api/1.0";
        }

        this.state = {
            searchParameters: {
                searchedPlacename: null,

                // checkboxes
                label: true,
                "old-labels": true,
                desc: false
            },
            searchResult: null,

            error: null
        };

    }

    componentDidMount() {

    }

    performSearch() {
        const params = this.state.searchParameters;
        if (params.searchedPlacename && params.searchedPlacename.length >= 3) {

            document.getElementById("search-button").classList.remove("is-loading");
            let url = null;


            if (params["old-labels"]) {
                url = `${this.api_base_url}/search?index=placename,placename_old_label&query=${params.searchedPlacename}&sort=placename.label,placename_old_label.rich_label`;
            } else {
                url = `${this.api_base_url}/search?index=placename&query=${params.searchedPlacename}&sort=placename.label`;
            }

            //clear results
            this.setState({
                ...params,
                searchResult: null,
                error: null
            });
            this.props.onSearch(this.state.searchResult);

            //fetch new results
            console.log("search urls: ", url);

            if (url) {
                document.getElementById("search-button").classList.add("is-loading");
                fetch(url)
                .then(res => {
                    if (!res.ok) {
                        throw res;
                    }
                    return res.json();
                })
                .then((result) => {
                    const oldResult = this.state.searchResult ? this.state.searchResult : [];
                    let newResult = result;

                    //console.log(oldResult, newResult);

                    Array.prototype.push.apply(newResult, oldResult);

                    //console.log(oldResult, newResult);

                    this.setState({
                        ...params,
                        searchResult: newResult,
                        error: null
                    });
                    this.props.onSearch(this.state.searchResult);
                    console.log(newResult.data.length);

                    document.getElementById("search-button").classList.remove("is-loading");
                })
                .catch(error => {
                    console.log("error while searching placename:", error);
                    document.getElementById("search-button").classList.remove("is-loading");
                    this.setState({error: error.statusText});
                });
            }

        }
    }


    handleLabelChange(e){
        /*
            when the state of the Label checkbox changes
        */
        this.setState({
            ...this.state,
            searchParameters : {
                ...this.state.searchParameters,
                label: e.target.checked
            }
        });
    }


    handleOldLabelsChange(e){
        /*
            when the state of the OldLabel checkbox changes
        */
        this.setState({
            ...this.state,
            searchParameters : {
                ...this.state.searchParameters,
                "old-labels": e.target.checked
            }
        });
    }

    handleDescChange(e){
        this.setState({
            ...this.state,
            searchParameters : {
                ...this.state.searchParameters,
                desc: e.target.checked
            }
        });
    }

    handlePlacenameChange(){
        this.setState({
            ...this.state,
            searchParameters : {
                ...this.state.searchParameters,
                searchedPlacename: document.getElementById("placenameInput").value
            }
        });
    }

    handleOnKeyPress(e) {
        /*
            When the user press Enter in the placename search box
        */
        if (e.key === 'Enter'){
            this.handlePlacenameChange();
        }
    }

    handleOnSearchClick() {
        this.handlePlacenameChange();
    }

    componentDidUpdate(prevProps, prevState) {
        // check if data has changed
        if (this.state.searchParameters !== prevState.searchParameters) {
            this.performSearch();
        }
    }

    render() {
        return (
            <div id="search-form-container">

                <div className="columns">
                    <div className="column">
                        <div className="field is-horizontal">
                            <div className="field-body">
                                <div className="field has-addons">
                                    <div className="control">
                                        <button id="search-button" className="button is-info" onClick={this.handleOnSearchClick}>
                                           <i className="fas fa-search"></i>
                                        </button>
                                    </div>
                                    <div className="control">
                                        <input id="placenameInput" className="input" type="text" placeholder="ex: Abancourt"
                                               onKeyPress={this.handleOnKeyPress}/>
                                    </div>
                                </div>
                            </div>
                        </div>
                         {/*
                        <div className="field is-horizontal">
                            <div className="field-label">
                                <label className="label">Inclure</label>
                            </div>
                            <div className="field-body">
                                <div className="field">
                                    <div className="control">

                                        <label className="checkbox">
                                            <input type="checkbox" name="member" value="label"
                                                   onChange={this.handleLabelChange}
                                                   defaultChecked={this.state.searchParameters.label}/>
                                               Vedette
                                        </label>

                                        <label className="checkbox">
                                            <input type="checkbox" name="member" value="old-labels" onChange={this.handleOldLabelsChange} defaultChecked={this.state.searchParameters["old-labels"]}/>
                                                Formes anciennes
                                            <span id="old-label-legend"></span>
                                        </label>

                                        <label className="checkbox">
                                            <input type="checkbox" name="member" value="desc" onChange={this.handleDescChange} defaultChecked={this.state.searchParameters.desc}/>
                                                description
                                        </label>

                                    </div>
                                </div>
                            </div>
                        </div>
                        */}

                    </div>

                    <div className="column"></div>
                </div>
            </div>
        );
    }

}

export default PlacenameSearchForm;