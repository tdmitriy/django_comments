$(document).ready(function () {

    // detect click on reply link
    $('.comments-wrapper').on('click', '.comment-reply-link', function (e) {
        e.preventDefault();
        var $replyLink = $(this);

        showOrHideReplyForm($replyLink);

        var rootId = $replyLink.attr('data-root-id');
        var parentId = $replyLink.attr('data-parent-id');
        parentId = parentId === undefined ? null : parentId;
        setValuesToForm(rootId, parentId);

    });


    function showOrHideReplyForm($replyLink) {
        var replySelector = '#reply_template';
        var $replyBox = $(replySelector);

        if (!$replyLink.next(replySelector).length) {
            $replyBox.hide();
            $replyBox.insertAfter($replyLink);
            $replyBox.slideToggle();
        } else {
            $replyBox.slideToggle();
        }
    }

    function setValuesToForm(rootId, parentId) {
        var $replyForm = $('#reply_form');
        clearForm('#reply_form');

        $replyForm.find('input[name="root_id"]').val(rootId);
        $replyForm.find('input[name="parent_id"]').val(parentId);
    }

    function postComment(isReplyForm) {
        var formId = isReplyForm === true ? '#reply_form' : '#post_comment_form';

        $(formId).submit(function (e) {
            var postData = $(this).serializeArray();
            var formURL = $(this).attr("action");
            $.ajax(
                {
                    url: formURL,
                    type: "POST",
                    data: postData,
                    success: function (data, textStatus, jqXHR) {
                        console.log("POSTED!", data, textStatus);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        console.error(errorThrown, textStatus);
                    }
                });
            e.preventDefault();
            e.unbind();

            clearForm(formId)
        });
    }

    function clearForm(formId) {
        $(formId).trigger("reset");
    }
});