// const Map = (props) => {
//   // This example creates a simple polygon representing the Bermuda Triangle.
//   var myLatlng = new google.maps.LatLng(-34.397, 150.644);
//   var mapOptions = {
//     zoom: 8,
//     center: myLatlng,
//     mapTypeId: "satellite",
//   };
//   var map = new google.maps.Map(document.getElementById("map"), mapOptions);
//   map.setMapTypeId("terrain");
// };

// export default Map;

// import { withGoogleMap, GoogleMap, Marker } from "react-google-maps";

// const PloygonMap = withGoogleMap((props) => (
//   <GoogleMap defaultZoom={8} defaultCenter={{ lat: -34.397, lng: 150.644 }}>
//     <Marker position={{ lat: -34.397, lng: 150.644 }} />
//   </GoogleMap>
// ));

// export default PloygonMap;

import {
  GoogleMap,
  Polygon,
  withScriptjs,
  withGoogleMap,
  TrafficLayer,
} from "react-google-maps";
import MarkerWithLabel from "react-google-maps/lib/components/addons/MarkerWithLabel";
import compose from "recompose/compose";
import withProps from "recompose/withProps";

const parseCoordinates = (coordinates) => {
  var result = [];
  for (var index = 0; index < coordinates.length - 1; index++) {
    result.push({
      lat: Number(coordinates[index].lat),
      lng: Number(coordinates[index].lng),
    });
  }
  return result;
};

const GoogleMapComponent = (function Map() {
  return compose(
    withProps((props) => ({
      googleMapURL:
        "https://maps.googleapis.com/maps/api/js?key=" +
        process.env.REACT_APP_GOOGLE_API_KEY +
        "&v=3.exp&libraries=geometry,drawing,places",
      loadingElement: props.loadingElement,
      containerElement: props.containerElement,
      mapElement: props.mapElement,
    })),
    withScriptjs,
    withGoogleMap
  )((props) => (
    <GoogleMap
      mapTypeId={props.mapType}
      defaultCenter={{
        lat: props.defaultCentre
          ? Number(props.defaultCentre.lat)
          : -33.83001256324069,
        lng: props.defaultCentre
          ? Number(props.defaultCentre.lng)
          : 151.182493988605,
      }}
      //note different spellings of centre and center.
      {...(props.centre && { center: props.centre })}
      defaultZoom={props.defaultZoom}
      zoomControl={false}
      tilt={props.tilt}
    >
      {props.isMarkerShown &&
        props.polygons &&
        props.polygons.map((poly, i) => {
          const onClick = props.onClick.bind(this, poly);
          return (
            <MarkerWithLabel
              position={{
                lat: poly.suburbCentre.lat,
                lng: poly.suburbCentre.lng,
              }}
              onClick={onClick}
              labelAnchor={new window.google.maps.Point(0, 0)}
              labelStyle={{
                backgroundColor: "white",
                fontSize: "12px",
                padding: "8px",
                borderRadius: "5px",
              }}
            >
              <div>{poly.metaData.name}</div>
            </MarkerWithLabel>
          );
        })}

      {props.individualGeoCode && (
        <MarkerWithLabel
          position={{
            lat: props.individualGeoCode.lat,
            lng: props.individualGeoCode.lng,
          }}
          labelAnchor={new window.google.maps.Point(0, 0)}
          labelStyle={{
            backgroundColor: "white",
            fontSize: "12px",
            padding: "8px",
            borderRadius: "5px",
          }}
        >
          <div>{props.markerTag}</div>
        </MarkerWithLabel>
      )}

      {props.showTrafficLayer && <TrafficLayer autoUpdate />}

      {props.isSuburbHighlighted &&
        props.polygons &&
        props.polygons.map((poly, i) => {
          const onClick = props.onClick.bind(this, poly);

          return (
            <Polygon
              path={parseCoordinates(poly.boundaries)}
              key={i}
              options={{
                fillColor: "yellow",
                fillOpacity: 0.4,
                strokeColor: "#d35400",
                strokeOpacity: 0.8,
                strokeWeight: 3,
              }}
              onClick={() => {
                onClick(poly);
              }}
            />
          );
        })}
    </GoogleMap>
  ));
})();

export default GoogleMapComponent;
