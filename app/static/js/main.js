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

$.fn.extend({
    disable: function (state) {
        return this.each(function () {
            this.disabled = state;
        });
    }
});


function setAlert(title, message, error = false, timeout = 3000) {
    let alert = $("#submit-alert")
    alert.find('#alert-message').text(message)
    alert.find('#alert-label').text(title)
    if (error) {
        alert.removeClass('alert-success').addClass('alert-danger')
        // alert.find('#alert-label').text('Error')
    } else {
        alert.removeClass('alert-danger').addClass('alert-success')
        // alert.find('#alert-label').text('Success')
    }

    alert.slideDown()

    // if (timeout > 0) {
    //     setInterval(() => {
    //         alert.slideUp()
    //     }, timeout);
    // }
}

function disableStockBtns(state = true) {
    log('Disabling Buttons')
    $('[id ^=stock][id $=subbtn]').disable(state)
    $('[id ^=stock][id $=addbtn]').disable(state)
    $("#submit-btn").prop('disabled', state);
}


function errorCallback() {
    setAlert("Error", "Unable to process transaction", true)
}

function sucessCallback() {
    setAlert("Success", "Transactions processed", false)
}

function submitStock() {
    stocks = {}
    if (Object.keys(mocstock.change_stocks).length) {
        Object.keys(mocstock.change_stocks).forEach(key => {
            if (mocstock.change_stocks[key] != 0) {
                stocks[key] = mocstock.change_stocks[key]
                mocstock.change_stocks[key] = 0
            }
        });
    }
    if (Object.keys(stocks).length) {
        data = {
            stocks: stocks
        }
        asyncAjaxJSON(data,
            'api/update_user_stock',
            'POST',
            function () {
                disableStockBtns();
                $('#submit-spinner').toggleClass('d-none');
            },
            () => {
                disableStockBtns(false);
                $('#submit-spinner').toggleClass('d-none');
            },
            sucessCallback,
            errorCallback
        )
    } else {
        setAlert("", "No Transaction Performed", true)
    }
}


//Ajax Handling functions
function asyncAjaxJSON(payload, target, method, before, complete, success, error, metaData) {
    log('AJAX[%s] request to %s with payload %o and metaData %o', method, target, payload, metaData);
    $.ajax({
        url: target,
        type: method,
        data: JSON.stringify(payload),
        dataType: "json",
        contentType: "application/json",
        beforeSend: before(metaData),
        complete: complete(metaData),

        success: function (data) {
            success(data, metaData)
        },

        error: function (jqXHR, textStatus, errorThrown) {
            error(textStatus, errorThrown, metaData, jqXHR)
        }

    });
}

function handleStockClick(id, price, quantity) {
    this.log("handleStockClick", id, price, quantity)

    new_qt = mocstock.stocks[id] + quantity
    if (!(new_qt < 0)) {
        if (mocstock.money >= price * quantity) {
            mocstock.money -= price * quantity
            mocstock.stocks[id] += quantity
            mocstock.change_stocks[id] += quantity

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
            mocstock.stocks[stock_id] = parseInt($(`#stock${stock_id}count`).text())
            mocstock.change_stocks[stock_id] = 0
            $(this).click(() => { handleStockClick(stock_id, price, quantity) })
        }
    );
    $('#submit-btn').click(() => {
        submitStock()
    });

}

$(document).ready(function () {
    $('#submit-spinner').toggleClass('d-none');
    mocstock.money = parseFloat($('#total_money').text());
    mocstock.stocks = {}
    mocstock.change_stocks = {}
    createOnclicks("addbtn")
    createOnclicks("subbtn")
});

