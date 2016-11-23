$(document).ready(function () {


    // detect click on reply link
    $('.comment-reply-link').click(function (e) {
        e.preventDefault();
        var $replyLink = $(this);

        showOrHideReplyForm($replyLink);

        var comment_id = $replyLink.attr('data-comment-id');
        var parent_id = $replyLink.attr('data-parent-id');
        parent_id = parent_id === undefined ? '' : parent_id;

        setValuesToReplyForm(comment_id, parent_id);

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

    function setValuesToReplyForm(comment_id, parent_id) {
        var replySelector = '#reply_form';
        var $replyForm = $(replySelector);

        $replyForm.find('input[name="comment_id"]').val(comment_id);
        $replyForm.find('input[name="parent_id"]').val(parent_id);
    }
});