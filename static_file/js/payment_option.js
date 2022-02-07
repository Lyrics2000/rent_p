function check_which(){
    var radioValue = $("input[id='bc1']:checked").val();
        if(radioValue){
            const v = $('#payment_collection')
            v.empty()

            const epp = `<div class="input_group">
            <div class="input_box">
                <input type="tel" name="" class="name" placeholder="Card Number 1111-2222-3333-4444" required>
                <i class="fa fa-credit-card icon"></i>
            </div>
        </div>
        <div class="input_group">
            <div class="input_box">
                <input type="tel" name="" class="name" placeholder="Card CVC 632" required>
                <i class="fa fa-user icon"></i>
            </div>
        </div>
        <div class="input_group">
            <div class="input_box">
                <div class="input_box">
                    <input type="number" placeholder="Exp Month" required class="name">
                    <i class="fa fa-calendar icon" aria-hidden="true"></i>
                </div>
            </div>
            <div class="input_box">
                <input type="number" placeholder="Exp Year" required class="name">
                <i class="fa fa-calendar-o icon" aria-hidden="true"></i>
            </div>
        </div>`

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