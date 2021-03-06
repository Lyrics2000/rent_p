  

  var MYLIBRARY = MYLIBRARY || (function(){
    var _args = {}; // private

    return {
        init : function(Args) {
            _args = Args;
            // some other initialising
        },
        getALlCards : function() {
        $("#warning").empty()
        var card_container  =  $('#card-container')
        var cont = $("#cont")
        card_container.empty();

    const holder = ` <div style="height: 400px;" class="box">
            <div class="image-container skeleton">
                <div style="width:100px;height:200px" class="image_holder skeleton"></div>
               
               
            </div>
            <div class="content">
                    
                <div class="price">
                    <h3 style="width: 15rem;height: 20px;" class="skeleton"></h3>
                    <div style="width: 5rem ; height: 20px;" class="skeleton"></div>
                  
                </div>
                <div class="location">
                    <h3 style="width: 20rem;height: 20px;" class="skeleton"></h3>
                    <p style="width: 20rem;height: 20px; margin-top: 10px;" class="skeleton"></p>
                </div>
              
                <div class="buttons">
                    <a href="#" class="btn skeleton"></a>
                    <a href="#" class="btn skeleton"></a>
                </div>
            </div>
        </div>`

    for(let i = 0;i<8;i++){
        card_container.append(holder)
    } 


$.ajax({
    type: 'POST',
    data : _args[0],
    url: _args[1],
    success: function (response) {
        console.log(response)
        card_container.empty();

    if(response.length > 0){
        

        
        // on successfull creating object
         // 1. clear the form.
        var dataa = response
        all_rooms_list = response

        for (let j = 0; j < dataa.length; j++) {
            var r = dataa[j];
            console.log(r)

            var elm = `<div  onmouseover="bigImg(this)" onmouseout="normalImg(this)" class="box">
            <input type="hidden" id="hidden_id" value="${r.id}">
        <div class="image-container">
            <img src="${r.room_picture}" alt="">
            
           
        </div>
        <div class="content">
            <div class="price">
                <h3>Ksh : ${r.rent}/mo</h3>
                <!-- <a href="{{r.get_saved_rentals}" class="fas fa-heart shinning"></a> -->
                <a style="background: red;color: white;" href="${r.get_unsaved_rentals}" class="fas fa-heart"></a>
           
            </div>
            <div class="location">
                <h3>${r.building.building_name}(${r.room_name})</h3>
            
            </div>
            <div style="flex-wrap:wrap;" class="details">
                ${r.room_size ? `<h3> <i class="fas fa-expand"></i> ${r.room_size} sqft </h3>` : `` }
                ${r.room_type ? `<h3> <i class="fas fa-bed"></i> ${r.room_type} </h3>` : `` }
            
                ${r.bathtab_np ? `<h3> <i class="fas fa-bath"></i> ${ r.bathtab_np} bathtab </h3>` : `` }
            
                ${r.balcony ? `<h3> <i class="fas fa-door-closed"></i>balcony </h3>` : `` }
                ${r.building.tv_connection ? `<h3> <i class="fas fa-tv"></i> tv connection </h3>` : ``}
                ${r.building.security ? `<h3> <i class="fas fa-key"></i> security </h3> ` : `` }

            </div>
            <div class="buttons">
                <a href="book_request/${r.id}/" class="btn">Book Tour</a>
                <a href="room_detailed/${r.id}/" class="btn">view details</a>
           
            </div>
        </div>
    </div>

`
           
            
      card_container.append(elm)

            
        
            
            

            //card_container.append(element)
          }

        
        // display the newly friend to table.
        // var instance = JSON.parse(response);

    }else{
       const w =  $("#card-container").empty()
       card_container.empty();
       w.append(`<div  class="information">
        <h1>We don't have houses in this area at this time</h1>
        <P>Please try to search again</P>

        <div class="image-container">
            <img src="https://www.trulia.com/images/txl3R/placeholder_images/NoResult.svg" alt="">
        </div>

        <div class="text-container">
            <div class="near_etsate">
                <h3>Near Houses</h3>
                <ul>
                    <li ><button onclick="getLocation('Single Room')"  style="cursor:pointer" >Single room near me</button></li>
                    <li><button onclick="getLocation('Double Room')" style="cursor:pointer"> Bouble Room room near me</button></li>
                    <li><button onclick="getLocation('BedSitter')" style="cursor:pointer">BedSitter room near me</button></li>
                    <li><button onclick="getLocation('1 Bedroom')" style="cursor:pointer">1 Bedroom room near me</button></li>
                    <li><button onclick="getLocation('2 Bedroom')" style="cursor:pointer">2 Bedroom room near me</button></li>
                    <li><button onclick="getLocation('3 Bedroom')" style="cursor:pointer">3 Bedroom room near me</button></li>
                    <li><button onclick="getLocation('4 Bedroom')" style="cursor:pointer">4 Bedroom room near me</button></li>
                </ul>
            </div>

            <div class="near_etsate">
                <h3>Near Houses By Location</h3>
                <ul>
                    <li><button onclick="getBuildingbyLocation(-1.286389,36.817223,'Nairobi, Kenya')" style="cursor:pointer;">Houses in Nairobi</button></li>
                    <li><button  onclick="getBuildingbyLocation(-1.286389,36.817223,'Kisumu,Nyanza, Kenya')"  style="cursor:pointer;">Houses In kisumu</button></li>
                    <li><button onclick="getBuildingbyLocation(-1.286389,36.817223,'Mombasa, Coastal Kenya, Kenya')"  style="cursor:pointer;">Houses in Mombasa</button></li>
                    <li><button onclick="getBuildingbyLocation(-1.286389,36.817223,'Nakuru,Kenya')"  style="cursor:pointer;">Houses in Nakuru</button></li>
                </ul>
            </div>
        </div>

    
    </div>`)

    }

      
       
        

      
      
    },
    error: function (response) {
        // alert the error if any error occured
        alert(response["responseJSON"]["error"]);
    }
})




        
        }
    };
}());
  
  
  
  
  
  

