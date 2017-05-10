$(document).ready(function(){
    $('input[type=radio][name=reward-option]').change(function() {
        if (this.value == 'yes-reward') {
            $('#new-reward-list').removeClass('nodisplay');
        }
        else if (this.value == 'no-reward') {
            $('#new-reward-list').addClass('nodisplay');
        }
    });
});

var $text1 = $('#process_text_1');
var $circle_1 = $('#circle_1');
var $process_text = $('#process_text');

$text1.waypoint(function(direction) {
    if (direction == 'down'){
        $circle_1.addClass('on_1');
        $text1.addClass('animated fadeInUp');
        $process_text.addClass('show');
    } else {
    $circle_1.removeClass('on_1');
    $text1.removeClass('animated fadeInUp');
    }
}, {offset:'90%'});

var $text2 = $('#process_text_2');
var $circle_2 = $('#circle_2');

$text2.waypoint(function(direction) {
    if (direction == 'down'){
        $circle_2.addClass('on_2');
        $text2.addClass('animated fadeInUp');
    } else{
    $circle_2.removeClass('on_2');
    $text2.removeClass('animated fadeInUp');
    } 
},{offset:'40%'});


var $text3 = $('#process_text_3');
var $circle_3 = $('#circle_3');

$text3.waypoint(function(direction) {
    if (direction == 'down'){
        $circle_3.addClass('on_3');
        $text3.addClass('animated fadeInUp');
    } else {
    $circle_3.removeClass('on_3');
    $text3.removeClass('animated fadeInUp');
    }
}, {offset:'40%'});

var $text4 = $('#process_text_4');

$text4.waypoint(function(direction) {
    if (direction == 'down'){
        $text4.addClass('show animated fadeInUp');
    } else {
        $text4s.removeClass('show animated fadeInUp');
    }
}, {offset:'40%'});

// var $cards = $('.cards');
// var $ready = $('#ready');

// $ready.waypoint(function(direction){
//     if (direction == 'down'){
//         $cards.addClass('animated fadeInUp');
//     } else {
//         $cards.removeClass('animated fadeInUp');
//     }
// }, {offset:'10%'});


