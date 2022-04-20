import React from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker
} from "react-simple-maps";

const geoUrl =
  "https://raw.githubusercontent.com/zcreativelabs/react-simple-maps/master/topojson-maps/world-110m.json";

class MapChart extends React.Component {

  constructor(){
    super();
    this.state = {
      geos: []
    }
  }
  componentDidMount(){
    fetch("http://localhost:5000/usersgeo").then(
      res => res.json()
    ).then(
      result => {
        this.setState({geos:result.result})
      }
    )
  }
  render(){
    return (
      <ComposableMap>
      <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map(geo => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill="#DDD"
                stroke="#FFF"
              />
            ))
          }
        </Geographies>
      {
        this.state.geos.map((item) => {
          return <Marker coordinates={[item[0], item[1]]}>
          <circle r={8} fill="#F53" />
        </Marker>
        })
      }
      
      </ComposableMap>
    );
  }

};

export default MapChart;