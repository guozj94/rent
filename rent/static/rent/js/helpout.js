var selectItem;
var requestingItem;
function getSelectItem() {
	$(document).on("click", "ul li", function() {
        var selectItemName = $(this).find("a").text();
        console.log("here");
		selectItem = $(this).parent().find("input").val();
        $("#dropdown-btn").text(selectItemName);
	});
}

function getRequestingItem() {
	requestingItem = $("section input").first().val();
}

function submitOffer() {
	getRequestingItem();
	$(document).on("click", "#submit-offer", function() {
		$.ajax({
			url: "/rent/submit_offer",
			type: "POST",
			data: "selectItem="+selectItem+"&requestingItem="+requestingItem+"&csrfmiddlewaretoken="+getCSRFToken(),
			dataType: "JSON",
			success: confirm,
			error: errorThrow,
		});
	});
}

function confirm() {
	$("#ICanHelp-Modal").append('<div class="vertical-alignment-helper">'+
                                	'<div class="modal-dialog vertical-align-center">'+
                                
                                    '<!-- Modal Content-->'+
                                    '<div class="modal-content container">'+
                                        '<div class="modal-header margin-between-element">'+
                                            '<button type="button" class="close" data-dismiss="modal">&times;</button>'+
                                            '<div class="h4 modal-title notification">A notification has been sent to the requester</div>'+
                                        '</div>'+
                                        '<div class="row margin-between-element">'+
                                            '<div class="modal-body">'+
                                                '<p class="center col-lg-8 col-md-8 col-sm-8 col-xs-8">This transaction has been added to My Offers page. Please contact the requester to discuss more details about the item, exchange location and payment.</p>'+
                                            '</div>'+
                                        '</div>'+
                                        '<div class="modal-footer row margin-between-element">'+
                                            '<div class="col-lg-3 col-md-3 col-sm-3 col-xs-3"></div>'+
                                            '<button type="button" class="btn btn-primary btn-primary-blue col-lg-3 col-md-3 col-sm-3 col-xs-3">Go to My Offers</button>'+
                                            '<button type="button" class="btn btn-primary btn-primary-blue col-lg-3 col-md-3 col-sm-3 col-xs-3" data-dismiss="modal">Contact Requester</button>'+
                                             '<div class="col-lg-3 col-md-3 col-sm-3 col-xs-3"></div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>');
}

function errorThrow() {
	$("#ICanHelp-Modal").append(
								'<div class="vertical-alignment-helper">'+
                                	'<div class="modal-dialog vertical-align-center">'+
                                
                                    '<!-- Modal Content-->'+
                                    '<div class="modal-content container">'+
                                        '<div class="modal-header margin-between-element">'+
                                            '<button type="button" class="close" data-dismiss="modal">&times;</button>'+
                                            '<div class="h4 modal-title notification">Unable to send.</div>'+
                                        '</div>'+
                                        '<div class="row margin-between-element">'+
                                            '<div class="modal-body">'+
                                                '<p class="center col-lg-8 col-md-8 col-sm-8 col-xs-8">Oops Sorry. An error occurs. Please try again later, or contact our customer service.</p>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>');

}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

$(document).ready(function() {
    getSelectItem();
    submitOffer();
});