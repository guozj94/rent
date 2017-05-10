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