
$(window).on('load',function(){
    if ($('#delete_password-error').length) {
        $('#delete-account-modal').modal('show');
    }
});

$(document).ready(function() {
    $('#flashedModal').modal('show');
    $('[data-toggle="tooltip"]').tooltip()


    $('.price-popover').popover({
        content: "We recommend making your listing free, people are more likely to claim it and we'll do better at preventing food waste!",
        html: true,
        placement: 'top',
        trigger: 'focus'
    });

    $('#listing-price').on('click', function() {
        $('.price-popover').popover();
    });


    $('#btn-prev').on('click', function(e) {
        if (pageCount > 0) {
            pageCount--;
            changePage(pageCount, "prev", getPageLength($(this), 3));
        }
    });


    $('.strength-popover').popover({
        content: "Your password must have" + 
                "<br />" +
                "<ul><li>6 or more characters</li> <li>Upper & lowercase letters</li> <li>At least one number & symbol</li></ul>" +
                '<div class="progress font-weight-bold" style="height: 20px;"><div class="progress-bar bg-danger" id="password-strength-bar" role="progressbar" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div></div>',
        html: true,
        placement: 'top',
        trigger: 'focus'
    });

    var currentStength = 0;
    var strengths = [['Weak', 'bg-danger'], ['Fair', 'bg-warning'], ['Good', 'bg-primary'], ['Strong', 'bg-success'], ['Perfect', 'bg-success']];


    $('#password, #about_you-password').on('click', function(e){    
        $('.strength-popover').popover('toggle');

        var strength = 10 / (10 / (currentStrength * 2)) * 10;

        $('#password-strength-bar').css("width", strength + '%');
        $('#password-strength-bar').text(strengths[currentStrength - 1][0]);
        $('#password-strength-bar').removeClass();
        $('#password-strength-bar').addClass('progress-bar');
        $('#password-strength-bar').addClass(strengths[currentStrength - 1][1]);
    });

    $('#password, #about_you-password').on('input', function(e){
        var passwordStrength = 1;

        var input = $('#password, #about_you-password').val();
        $('#password-strength').removeClass('d-none');

        if (input.length > 0) {
            if (input.length >= 6) {
                passwordStrength += 1;
            }
    
            if (hasCapital(input)) {
                passwordStrength += 1;
            } 

            if (hasCharacter(input)) {
                passwordStrength += 1;
            }
   
            if (hasNumber(input)) {
                passwordStrength += 1;
            }
        } else {
            $('#password-strength').addClass('d-none');
        }

        currentStrength = passwordStrength;
        var strength = 10 / (10 / (passwordStrength * 2)) * 10;
       
        $('#password-strength-bar').css("width", strength + '%');
        $('#password-strength-bar').text(strengths[passwordStrength - 1][0]);
        $('#password-strength-bar').removeClass();
        $('#password-strength-bar').addClass('progress-bar');
        $('#password-strength-bar').addClass(strengths[passwordStrength - 1][1]);
    });
});

function hasNumber(string) {
    return /\d/.test(string);
}

function hasCapital(string) {
    for (var i = 0; i < string.length; i++) {
        if (string[i] === string[i].toUpperCase() && string[i] !== string[i].toLowerCase()) {
            return true;
        }
    }
    return false;
}

function hasCharacter(string) {
    for (var i = 0; i < string.length; i++) {
        if (string[i].match(/[-!$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/)) {
            return true;
        }
    }
    return false;
}