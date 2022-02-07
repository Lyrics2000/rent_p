function check_which(){
    var radioValue = $("input[id='bc1']:checked").val();
        if(radioValue){
            const v = $('#payment_collection')
            v.empty()

            const epp = `
            <div class="input_group">
                <div class="input_box">
                <input id="stripe_card" type="hidden" name="payment_option" value = "mpesa">
                </div>
            </div>
            
            <div id="card-element">
                <!-- A Stripe Element will be inserted here. -->
              </div>

              <!-- Used to display form errors. -->
              <div id="card-errors" role="alert"></div>
            `

    v.append(epp)

        }
    var radioValue2 = $("input[id='bc2']:checked").val();
    if(radioValue2){
        const v = $('#payment_collection')
        v.empty()

        const epp = `<div class="input_group">
        <div class="input_box">
        <input type="hidden" name="payment_option" value = "mpesa">
            <input type="tel" name="mpesa_payment" class="name" placeholder="Mpesa Phone Number" required>
            <i class="fa fa-phone icon"></i>
        </div>
    </div>`

    v.append(epp)
    }
}

// payment form submissions
$('#payment_form_form').submit(function (e) { 
    e.preventDefault();
    const indexed_array = {};
    const serialized_data = $('#payment_form_form').serializeArray();
    $.map(serialized_data, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    console.log(indexed_array)
    const appender  =  `<div class="loader" > </div>`
    const animation_holder  =  $('#animation_holder')
    const btn = $('#submit_btn')
    
    animation_holder.empty()
    animation_holder.append(appender)
    btn.empty()

    if(indexed_array.payment_option === "mpesa"){
        pay_with_mpesa(indexed_array);
    }


    
});