var updateBtns = document.getElementsByClassName('update-cart')
console.log(updateBtns)

// when click on up or down arrow button
for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:',action)
        console.log('USER:',user)
        if (user == 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}

// for gest user
function addCookieItem(productId,action){
    console.log('User is not authenticated')
	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}
		}else{
			cart[productId]['quantity'] += 1
		}
	}
    if(action=='remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity']==0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log('Cart:',cart)
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}

// for registered user
function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..')
    var url = '/update_item/'
    // generate csrftoken to avoid malicious attacks
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId,'action': action})
    })
    .then((response)=>{
        return response.json();
    })
    .then((data)=> {
        console.log('data:', data)
        location.reload()
    });
}