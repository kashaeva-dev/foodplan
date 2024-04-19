const order_form = document.getElementById('order');

order_form.onclick = (e) => {
    cost = document.getElementsByTagName('h3')[0];
    sum = 0;
    selects = document.getElementsByTagName('select');
    for (let i = 1; i <5; i++) {
        v = Number(selects[i].value);
        if (!v) {
            if (sum)
                sum += 10;
            else
                sum = 75;
        }
    }
    sum *= selects[0].value;
    cost.innerHTML = "Стоимость: "+sum+"₽";
};