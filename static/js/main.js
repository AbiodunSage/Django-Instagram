$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = jQuery.trim(cookies[i]);
                    if (cookie.startsWith(name + '=')) {
                        cookieValue = decodeURIComponent(cookie.split('=')[1]);
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:/.test(settings.url) || /^https:/.test(settings.url))) {
            let csrftoken = getCookie('csrftoken');
            if (csrftoken) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            } else {
                console.error("CSRF token not found!");
            }
        }
    }
});


$(document).on("click",".js-toggle-modal", function(e){
    e.preventDefault()
    $(".js-modal").toggleClass("hidden")
});
$('#file-input').on('change', function(event) {
    let file = event.target.files[0];
    let previewContainer = $('#preview-container');
    let imagePreview = $('#image-preview');
    let videoPreview = $('#video-preview');
    let uploadBox = $('#upload-box');

    if (file) {
        let fileType = file.type;
        previewContainer.show();
        uploadBox.hide();


        // Hide both previews initially
        imagePreview.hide();
        videoPreview.hide();

        let fileURL = URL.createObjectURL(file);

        if (fileType.startsWith('image/')) {
            imagePreview.attr('src', fileURL).show();
        } else if (fileType.startsWith('video/')) {
            videoPreview.attr('src', fileURL).show();
        }
    }
})

$(document).ready(function () {
    $(".js-submit").on("click", function (e) {
        e.preventDefault(); // Prevent default form submission

        let formData = new FormData();
        let fileInput = document.getElementById("file-input");
        let textInput = $(".text-input").val();
        let postUrl = $(".text-input").data("post-url");

        // Check if there are selected files
        if (fileInput.files.length > 0) {
            for (let i = 0; i < fileInput.files.length; i++) {
                formData.append("file", fileInput.files[i]);  // Append files
            }
        } else {
            alert("Please select a file before posting.");
            return;
        }

        formData.append("caption", textInput);  // Add caption

        // DEBUG: Print FormData contents
        for (let pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        // Get CSRF token from the meta tag
        let csrfToken = $("meta[name='csrf-token']").attr("content");

        $.ajax({
            url: postUrl,
            type: "POST",
            headers: { "X-CSRFToken": csrfToken }, // CSRF Token
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function () {
                $(".js-submit").text("Uploading...").prop("disabled", true);
            },
            success: function (response,dataHtml) {
                alert("Post created successfully!");
                $(".js-modal").addClass("hidden"); // Hide modal
                $(".text-input").val(""); // Clear input
                $("#file-input").val("");
               
                 // Replace input with cloned input
                $("#posts-container").prepend(response.html);
                
                // Reset file input
               
            },
            error: function (xhr) {
                console.error("Error:", xhr.responseText);
                alert("Failed to create post: " + xhr.responseText);
            },
            complete: function () {
                $(".js-submit").text("Post").prop("disabled", false);
            }
        });
    });
});
$(document).on("click",".js-follow",function(e) {
    e.preventDefault();
    const action = $(this).attr("data-action");
  
    $.ajax({
        type: 'POST',
        url: $(this).data("url"),
        data: {
            action: action,
            username: $(this).data("username"),
        },
        success: (data) => {
            $(".js-follow-text").text(data.wording);

            if(action == "follow"){
                $(this).attr("data-action","unfollow");
            }else{
                $(this).attr("data-action","follow"); 
            }
        },
        error: (error) => {
            console.warn(error);
            $(this).prop("disabled", false).text("Error");
        }
    });
});