function getResult() {
	$("#search-btn").click(function() {
		var keyword = $("#searchbar").val();
		if(keyword) {
			$.ajax({
				url: "/rent/search_ajax",
				type: "GET",
				data: "keyword="+keyword+"&csrfmiddlewaretoken="+getCSRFToken(),
				dataType: "JSON",
				success: updateResult,
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					alert("error");
					$("#items-container").text("nothing");
				}
			});
			$("#searchbar").val("");
		}
		else {
			$("#searchbar").val("");
			return;
		}
	});
}

function updateResult(list) {
	$("#items-container").empty();
	$.each(list, function() {
		appendItem(this.fields.name, this.fields.picture, this.fields.description, this.fields.reward, this.fields.lender, this.fields.lendername);
	});
	showResult();
}

function showResult() {
	var all_result = $(".an-item");
	var count = all_result.length;
	if(count <= 5) {
		$.each(all_result, function() {
			$(this).removeClass("nodisplay");
		});
		return;
	}
	else {
		all_result[0].removeClass("nodisplay");
		all_result[1].removeClass("nodisplay");
		all_result[2].removeClass("nodisplay");
		all_result[3].removeClass("nodisplay");
		all_result[4].removeClass("nodisplay");
		$("#more").removeClass("nodisplay");
	}
	var i = 5;
	$(document).on("click", "#more", function() {
		while(i + 5 < all_result.length) {
			all_result[i].removeClass("nodisplay");
			all_result[i+1].removeClass("nodisplay");
			all_result[i+2].removeClass("nodisplay");
			all_result[i+3].removeClass("nodisplay");
			all_result[i+4].removeClass("nodisplay");
			i = i + 5
		}
		if(i >= all_result.length) {all_result.removeClass("nodisplay"); $("#more").addClass("nodisplay");};
	});
}

function startRequest() {
	$("#send-request-btn").click(function() {
		$(this).addClass("nodisplay");
		$("#form").removeClass("nodisplay");
		$("#send").removeClass("nodisplay");
	});
}

function submitRequest() {
	var reward;
	$("#checkbox").click(function() {
			if(this.checked) {$("#reward").val(""); reward = "depends"; $("#reward").prop('disabled', true); return;}
			else {reward = null; $("#reward").prop('disabled', false); return;}
		});
	$(document).on("click", "#send", function() {
		var name = $("#i-am-looking-for").val();
		var description = $("#form-description").val();
		var from = $("#datetimepicker1 input").val();
		var to = $("#datetimepicker2 input").val();
		console.log(from);
		console.log(to);
		if(!name || !description) {
			if(!name) $("#i-am-looking-for").css("border", "solid 2px rgb(238,107,96)");
			if(!description) $("#form-description").css("border", "solid 2px rgb(238,107,96)");
			//if(!from) $("#datetimepicker1 input").css("border", "solid 2px rgb(238,107,96)");
			//if(!to) $("#datetimepicker2 input").css("border", "solid 2px rgb(238,107,96)");
			return;
		}
		if(reward == null) reward = $("#reward").val();
		$.ajax({
			url: "/rent/send_request_ajax",
			type: "POST",
			data: "name="+name+"&description="+description+"&from="+from+"&to="+to+"&reward="+reward+"&csrfmiddlewaretoken="+getCSRFToken(),
			dataType: "JSON",
			success: function() {
				$("#form").addClass("nodisplay");
				$("#send").addClass("nodisplay");
				$("#success-container").removeClass("nodisplay");
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
				alert("error");
				$("#items-container").text("nothing");
			}
		});
		
	});
}

function appendItem(name, pic, description, reward, lenderid, lendername) {
	$("#items-container").append(
		'<div class="an-item nodisplay">'+
            '<div class="row title">'+
                '<div class="col-md-1 col-sm-1 col-xs-1 item-image">'+
                    '<img src="'+pic+'" width="60px" height="60px"></img>'+
                '</div>'+
                '<div class="col-md-11 col-sm-11 col-xs-11 item-name">'+
                    '<div>'+name+'</div>'+
                '</div>'+
            '</div>'+
            '<div class="row description">'+
            	'<div class="col-md-1 col-sm-1 col-xs-12 row-title description-title">Description</div>'+
                '<div class="col-md-11 col-sm-11 col-xs-12 row-content description-content">'+
                    '<p>'+description+'</p>'+
                '</div>'+
            '</div>'+
            '<div class="row reward">'+
                '<div class="col-md-1 col-sm-1 col-xs-12 row-title reward-title">Reward</div>'+
                '<div class="col-md-11 col-sm-11 col-xs-12 row-content reward-content"><p>'+reward+'</p></div>'+
            '</div>'+
            '<div class="row lender">'+
                '<div class="col-md-1 col-sm-1 col-xs-12 row-title lender-title">Lender</div>'+
                '<div class="col-md-11 col-sm-11 col-xs-12 row-content lender-content">'+
                    '<div class="row lender-row">'+
                        '<div class="col-md-1 col-sm-2 col-xs-12">'+
                            '<img src="'+lender_image_url+'/'+lenderid+'" width="37px" height="37px">'+
                        '</div>'+
                    	'<div class="col-md-10 col-sm-9 col-xs-12 lender-name">'+lendername+'</div>'+
                        '<div class="col-md-10 col-sm-9 col-xs-12 lender-rate">stars here</div>'+
                    '</div>'+
                '</div>'+
            '</div>'+
            '<div class="row">'+
                '<div class="col-md-10"></div>'+
                '<div class="col-md-2 request-btn-container">'+
                    '<input type="hidden" id="itemid" name="itemid" value="{{item.id}}">'+
                    '<div class="request-btn clickable">Request</div>'+
                '</div>'+
            '</div>'+
        '</div>'
		);
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
	getResult();
	startRequest();
	submitRequest();
});