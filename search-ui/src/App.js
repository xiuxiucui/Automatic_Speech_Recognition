
import React from "react";
import {
    ErrorBoundary,
    Facet,
    SearchProvider,
    SearchBox,
    Results,
    PagingInfo,
    ResultsPerPage,
    Paging,
    Sorting,
    WithSearch
} from "@elastic/react-search-ui";
import {
    BooleanFacet, Layout, SingleLinksFacet, SingleSelectFacet
} from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";
import {SearchDriverOptions} from "@elastic/search-ui";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

const connector = new ElasticsearchAPIConnector({
    host: "http://localhost:9200",
    index: "generated_text",
    // apiKey:""
});


const config = {
    searchQuery: {
        search_fields: {
            filename:{},
            generated_text: {
                weight: 3
            },
            accent: {},
            age: {},
            gender: {}
        },
        result_fields: {
            filename: {
                snippet: {}
            },
            generated_text: {
                snippet: {}
            },
            accent: {
                snippet: {}
            },
            age: {
                snippet: {}
            },
            gender: {
                snippet: {}
            },
            duration: {
                snippet: {}
            }

        },
        disjunctiveFacets: [
            "age.keyword",
            "gender.keyword",
            "accent.keyword"
        ],
        facets: {
            "age.keyword": { type: "value" },
            "gender.keyword": { type: "value" },
            "accent.keyword": { type: "value" },
            duration:{
                type: "range",
                ranges:[
                    { from: -1, name: "Any" },
                    { from: 0, to: 5, name: "1 to 5 second" },
                    { from: 5.00001, to: 10, name: "5 to 10 second" },
                    { from: 10.00001, to: 20, name: "10 to 20 second" },
                    { from: 20.00001,  name: "More than 20" }
                ]
            }
        }
    },
    apiConnector: connector,
    alwaysSearchOnInitialLoad: true
};
export default function App() {
    return (
        <SearchProvider config={config}>
            <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
                {({ wasSearched }) => {
                    return (
                        <div className="App">
                            <ErrorBoundary>
                                <Layout
                                    header={
                                        <SearchBox
                                            // autocompleteMinimumCharacters={3}
                                            // autocompleteResults={{
                                            //     linkTarget: "_blank",
                                            //     sectionTitle: "Results",
                                            //     filenameField: "filename",
                                            //     ageField: "age",
                                            //     durationField: "duration",
                                            //     accentField: "accent",
                                            // }}
                                            autocompleteSuggestions={false}
                                            debounceLength={0}
                                        />
                                    }
                                    sideContent={
                                        <div>
                                            {/*{wasSearched && (*/}
                                            {/*    <Sorting label={"Sort by"} sortOptions={[]} />*/}
                                            {/*)}*/}
                                            <Facet
                                                key={"1"}
                                                field="age.keyword"
                                                label="Age"
                                                filterType="any"
                                                isFilterable={true}
                                            />
                                            <Facet
                                                key={"2"}
                                                field="gender.keyword"
                                                label="Gender"
                                                filterType="any"
                                                isFilterable={true}
                                            />
                                            <Facet
                                                key={"3"}
                                                field="accent.keyword"
                                                label="Accent"
                                                filterType="any"
                                                isFilterable={true}
                                            />
                                            <Facet
                                                key={"4"}
                                                field="duration"
                                                label="Duration"
                                                filterType="any"
                                                isFilterable={true}
                                            />
                                        </div>
                                    }
                                    bodyContent={<Results shouldTrackClickThrough={true}/>}
                                    bodyHeader={
                                        <React.Fragment>
                                            {wasSearched && <PagingInfo/>}
                                            {wasSearched && <ResultsPerPage/>}
                                        </React.Fragment>
                                    }
                                    bodyFooter={<Paging/>}
                                />
                            </ErrorBoundary>
                        </div>
                    );
                }}
            </WithSearch>
        </SearchProvider>
    );
}
