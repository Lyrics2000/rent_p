var MAPINITIALIZER = MAPINITIALIZER || (function(){
    var _args = {}; // private

    return {
        init : function(Args) {
            _args = Args;
            // some other initialising
            // main lat [{{main_lat}},{{main_lng}}],icon '{% static "images/mk.png" %}'
            // data {"criteria_location":'{{criteria_mk}}',"xminm":'{{xmin}}',"xmaxm":'{{xmax}}',"yminm":'{{ymin}}',"ymaxm":'{{ymax}}','csrfmiddlewaretoken': '{{ csrf_token }}'}
            //url "{% url 'homepage:all_rm' %}"
            //coordinates = {{coordinates}}

        },
        initializeMap : function() {
            // map = L.map( 'map', {
            //     center: [_args[0],_args[1]],
            //     minZoom: 1,
            //     zoom: 15,
            //     zoomControl: true
            
            //     });
            coordinates = _args[5]
            
            console.log("coordinates",coordinates)
            const mmm = []
            coordinates.forEach(element => {
                mmm.push(element)
                
            });


            const bounds  = {
                "type": "FeatureCollection",
                "features": [
                  {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                      "type": "Polygon",
                      "coordinates":[
                      mmm
                           ]
                   
                    }
                  }
                ]
              };
            
              console.log("bounds",bounds)
            
              
             
             
              const b = bounds.features[0].geometry.coordinates[0];
            
            const latl = []
            var coordinates = bounds.features[0].geometry.coordinates[0];


            coordinates.forEach(eleme=> {
                const l = eleme;
                l.forEach(element => {
            
                    latl.push(new L.LatLng(parseFloat(element[1]), parseFloat(element[0])));
                });
                console.log("ll",l);
                
            });
            
            
            console.log("ppp",latl)
            
            
                L.Mask = L.Polygon.extend({
                options: {
                    stroke: true,
                    color: '#333',
                    fillOpacity: 0.6,
                    clickable: true,
            
            
                    outerBounds: new L.LatLngBounds([-90, -360], [90, 360])
                },
            
                initialize: function (latLngs, options) {
            
                     var outerBoundsLatLngs = [
                        this.options.outerBounds.getSouthWest(),
                        this.options.outerBounds.getNorthWest(),
                        this.options.outerBounds.getNorthEast(),
                        this.options.outerBounds.getSouthEast()
                    ];
                    L.Polygon.prototype.initialize.call(this, [outerBoundsLatLngs, latLngs], options);  
                },
            
            });
            L.mask = function (latLngs, options) {
                return new L.Mask(latLngs, options);
            };
            
            
            
        
            console.log("qqqq",mmm)
            L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
                maxZoom: 14,
                subdomains:['mt0','mt1','mt2','mt3']
            }).addTo(map);


            var smallIcon = new L.Icon({
                iconSize: [27, 27],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: _args[2]
            });
        


            const markers = L.markerClusterGroup({
                spiderfyShapePositions: function(count, centerPt) {
                        var distanceFromCenter = 75,
                            markerDistance = 70,
                            lineLength = markerDistance * (count - 1),
                            lineStart = centerPt.y - lineLength / 2,
                            res = [],
                            i;
        
                        res.length = count;
        
                        for (i = count - 1; i >= 0; i--) {
                            res[i] = new Point(centerPt.x + distanceFromCenter, lineStart + markerDistance * i);
                        }
        
                        return res;
                    }
        });
     
        const empty_l = [];
        var latLngs = [];


          
     $.ajax({
        type: 'POST',
        data : _args[3] ,
        url: _args[4],
        success: function (data) {

        console.log("new data",data)

        for (let n = 0; n < data.length; n++) {
            const el = data[n];
            const lat = el.building.geom.coordinates[0]
            const long = el.building.geom.coordinates[1]

            latLngs.push(new L.LatLng(lat, long));
            
        }





data.forEach(element => {

    const dicti2 = {
        type : "Feature",
        geometry : element.building.geom,
        properties : element
    }

    empty_l.push(dicti2)


    
});






const dicti = {
    type : "FeatureCollection",
    features : empty_l

}


console.log("looo",dicti)



var geojson = L.geoJson(dicti, {
    onEachFeature: function(feature, layer) {
         // create popup contents
        
         console.log(feature.properties.account_number)
    
         var cusp = `<div style="display: flex;flex-wrap: wrap;gap:1.5rem;width: 250px;height: 200px;">
    
    
    <div style="border:.1rem solid #000;box-shadow: 0 .5rem 1rem #000;border-radius: .5rem;overflow:hidden;background:#fff;flex:1 1 30rem;">
        <div style="overflow:hidden;position: relative;width: 100%;height: 10rem;">
            <img style="width: 100%;height: 200px;object-fit: cover;transition: .2s linear;" src="${feature.properties.room_picture}" alt="">
            <div style="position: absolute;top:10px; left:0;display: flex;">
              
                <h3 style="font-weight: 500;
                font-size: 10px;
                color:white;
                background:red;
                border-radius: .5rem;
                padding:.5rem ;
                margin-left: 1rem;">for rent</h3>
            </div>
           
        </div>
     
        <div >
                
            <div style=" display: flex;
            align-items: center;justify-content: space-between;margin-left: 20px;margin-right: 20px;">
                <h3 style="font-size:12px;">${feature.properties.room_name}</h3>
                <h3 style="font-size:12px;">Ksh${feature.properties.rent}/mo</h3>
                <div style="font-size:12px;" href="#" class="fas fa-heart shinning"></div>
              
            </div>
         
        
            <div style="display: flex;align-items: center; justify-content: space-evenly;margin-left: 10px;margin-right: 10px;">
                        <a style="padding:0.4rem; 0.8rem;font-size:1.3rem" href="book_request/${feature.properties.id}/" class="btn">Book Tour</a>
                        <a style="padding:0.4rem; 0.8rem;font-size:1.3rem" href="room_detailed/${feature.properties.id}/" class="btn">view details</a>
                   
                    </div>
        </div>
    </div>
    
    </div>
    `
    
        
    
       
        
            layer.bindPopup(cusp);
    
    
        },
    pointToLayer: function (feature, latlng) {
      
       const mark = markers.addLayer(L.marker(latlng, {icon: new L.divIcon({
        className: 'location-pin',
        html: `<div style="display:flex;align-items:center;justify-content:center;background:#fb4e2e;padding:1.5px;width:3.5vw;border-radius: 5px;">
            <div class="getUiSvgContainer__SvgContainer-sc-1cdn1ln-0 bDMRDK">
             
            </div><div style="font-size:10px;color:#fff;font-weight:400;line-height:1.8;">${feature.properties.rent > 1000 ? `${feature.properties.rent / 1000}K` : feature.properties.rent }/m</div></div>`,
        iconSize: [30, 30],
        iconAnchor: [18, 30]
      })}).on('mouseover',(e)=>{
            console.log(latlng)
          //  this.target.openPopup()
    
          var cusp = `<div style="display: flex;flex-wrap: wrap;gap:1.5rem;width: 250px;height: 200px;">
    
    
    <div style="border:.1rem solid #000;box-shadow: 0 .5rem 1rem #000;border-radius: .5rem;overflow:hidden;background:#fff;flex:1 1 15rem;">
        <div style="overflow:hidden;position: relative;width: 100%;height: 10rem;">
            <img style="width: 100%;height: 200px;object-fit: cover;transition: .2s linear;" src="${feature.properties.room_picture}" alt="">
            <div style="position: absolute;top:10px; left:0;display: flex;">
              
                <h3 style="font-weight: 500;
                font-size: 10px;
                color:white;
                background:red;
                border-radius: .5rem;
                padding:.5rem ;
                margin-left: 1rem;">for rent</h3>
            </div>
           
        </div>
     
        <div >
                
            <div style=" display: flex;
            align-items: center;justify-content: space-between;margin-left: 20px;margin-right: 20px;">
                <h3 style="font-size:12px;">${feature.properties.room_name}</h3>
                <h3 style="font-size:12px;">Ksh${feature.properties.rent}/mo</h3>
                <div style="font-size:12px;" href="#" class="fas fa-heart shinning"></div>
              
            </div>
         
        
            <div style="display: flex;align-items: center; justify-content: space-evenly;margin-left: 10px;margin-right: 10px;">
                        <a style="padding:0.4rem; 0.8rem;font-size:1.3rem" href="book_request/${feature.properties.id}/" class="btn">Book Tour</a>
                        <a style="padding:0.4rem; 0.8rem;font-size:1.3rem" href="room_detailed/${feature.properties.id}/" class="btn">view details</a>
                   
                    </div>
        </div>
    </div>
    
    </div>
    `
    
        
    
          
     
    
           
            var popup = L.popup()
                .setLatLng(e.latlng) 
                .setContent(cusp)
                .openOn(map);
            // var card_container  =  $('#card-container')
            // {% comment %} card_container.empty();
            // card_container.append(element) {% endcomment %}
    
        }));
    
        return mark
      }
    });
    
    
    geojson.addTo(map);
    
    map.fitBounds(latl); 
    
    
    if(latl.length > 0){
        L.mask(latl).addTo(map);
    
    }else{
    
        var circle = L.circle([_args[0],_args[1]], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0,
            radius: 6000
        }).addTo(map);
        
    
    }
    
    
    
    
    
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        })
    
        
        
        map.addLayer(markers);
       
      
    
        
    
    
    



   
        

        
        }
    };

    
}());