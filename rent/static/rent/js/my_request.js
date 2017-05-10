var currentShow = 0;
var slideGroups = [];

function floorplanSlide() {
	var all_floor_plan = $(".a-response-container");
	console.log(all_floor_plan);
	if(all_floor_plan.length <= 3) {
		$(".slide-right").css("display", "none");
		$(".slide-left").css("display", "none");
		return 0;
	}
	var count = 0;
	var group = [];
	for(var i=0; i < all_floor_plan.length; i++) {
		all_floor_plan[i].className += " nodisplay";
		if(group.length < 3) {
			group.push(all_floor_plan[i]);
		}
		else {
			slideGroups.push(group);
			group = [];
			group.push(all_floor_plan[i]);
		}
		if(i == all_floor_plan.length - 1) {
			slideGroups.push(group);
			group = []
		}
	}
	for(var i=0; i < slideGroups[0].length; i++) {
		slideGroups[0][i].classList.remove("nodisplay");
	}
	console.log(slideGroups[0][0]);
}

function floorplanSlideshow() {
	$(".slide-right").click(function() {
		console.log("right-btn clicked");
		for(var i=0; i < slideGroups[currentShow].length; i++) {
			slideGroups[currentShow][i].className += " nodisplay";
		}
		if(currentShow == slideGroups.length - 1) currentShow = 0;
		else currentShow++;
		for(var j=0; j < slideGroups[currentShow].length; j++) {
			slideGroups[currentShow][j].classList.remove("nodisplay");
		}
	});
	$(".slide-left").click(function() {
		console.log("left-btn clicked");
		for(var i=0; i < slideGroups[currentShow].length; i++) {
			slideGroups[currentShow][i].className += " nodisplay";
		}
		if(currentShow == 0) currentShow = slideGroups.length - 1;
		else currentShow--;
		for(var j=0; j < slideGroups[currentShow].length; j++) {
			slideGroups[currentShow][j].classList.remove("nodisplay");
		}
	});
}

$(document).ready(function() {
	floorplanSlide();
	floorplanSlideshow();
});
