mocstock = {};

//Logging functions
function log(...args) {
    if (window.console && window.console.log) {
        console.log(...args);
    }
}

$.fn.log = function (...args) {
    log(this, ...args);
    return this;
}


function submitStock() {
    stocks = {}
    if (Object.keys(mocstock.stocks).length) {
        Object.keys(mocstock.stocks).forEach(key => {
            if (mocstock.stocks[key] > 0) {
                stocks[key] = mocstock.stocks[key]
            }
        });
    }
    if (Object.keys(stocks).length) {
        data = {
            stocks: stocks
        }
        asyncAjaxJSON(data, 'api/update_stocks', 'POST')
    } else {
        log('No stock purchased')
    }
}


//Ajax Handling functions
function asyncAjaxJSON(payload, target, method, before, complete, sucess, error, metaData) {
    log('AJAX[%s] request to %s with payload %o and metaData %o', method, target, payload, metaData);
    $.ajax({
        url: target,
        type: method,
        data: JSON.stringify(payload),
        dataType: "json",
        contentType: "application/json",
        // beforeSend: before(metaData),
        // complete: complete(metaData),

        // success: function (data) {
        //     sucess(data, metaData)
        // },

        // error: function (jqXHR, textStatus, errorThrown) {
        //     error(textStatus, errorThrown, metaData, jqXHR)
        // }

    });
}

function handleStockClick(id, price, quantity) {
    this.log("handleStockClick", id, price, quantity)

    new_qt = mocstock.stocks[id] + quantity
    if (!(new_qt < 0)) {
        if (mocstock.money >= price * quantity) {
            mocstock.money -= price * quantity
            mocstock.stocks[id] += quantity
            $('#total_money').text(mocstock.money)
            $(`#stock${id}count`).text(mocstock.stocks[id])
        }
        else {
            log("Not Enought Money")
        }
    } else {
        log("No Stock to sell")
    }
}

function createOnclicks(suffix = "addbtn") {
    this.log("Creating Clicks for - " + suffix)
    $(`[id ^=stock][id $=${suffix}]`).each(
        function () {
            let stock_id = this['id'].replace("stock", "").replace(suffix, "")
            let price = parseFloat($(`[id ^=stock${stock_id}price]`).text().replace('₹', ''))
            let quantity = (suffix == "addbtn") ? 1 : -1
            mocstock.stocks[stock_id] = 0
            $(this).click(() => { handleStockClick(stock_id, price, quantity) })
        }
    );
}

$(document).ready(function () {
    mocstock.money = parseFloat($('#total_money').text());
    mocstock.stocks = {}
    createOnclicks("addbtn")
    createOnclicks("subbtn")
});

