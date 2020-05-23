console.log('hi')
var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        if (user === 'AnonymousUser') {
            addCookiItem(productId,action)
            console.log('AnonymousUser')
        }
        else {
            updateUserOrder(productId, action)
        }
    });
}

function addCookiItem(productId, action) {
    console.log('cookie cart')
    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        }
        else {
            cart[productId]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0){
            console.log('remove item')
            delete cart[productId]
        }
    }
    console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}


function updateUserOrder(productId, action) {
    var url = '/update-item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
        .then((Response) => {
            return Response.json()
        })
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}
