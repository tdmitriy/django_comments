$(document).ready(function () {

    // facebook has this hash tags on redirects, so remove them
    if (window.location.hash == '#_=_') {
        window.location.hash = '';
    }

    $('[data-toggle="tooltip"]').tooltip();

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
            // insert reply box when user clicked on 'reply' link
            $replyBox.insertAfter($replyLink);
            toggleReplyBox($replyBox);
        } else {
            toggleReplyBox($replyBox);
        }
    }

    function toggleReplyBox($replyBox) {
        $replyBox.slideToggle(function () {
            $('#reply_form').find('textarea').focus();
        });
    }

    function setValuesToReplyForm(comment_id, parent_id) {
        var replySelector = '#reply_form';
        var $replyForm = $(replySelector);
        $replyForm.trigger("reset");

        $replyForm.find('input[name="comment_id"]').val(comment_id);
        $replyForm.find('input[name="parent_id"]').val(parent_id);
    }
});