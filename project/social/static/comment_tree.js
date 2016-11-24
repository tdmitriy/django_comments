$(document).ready(function () {
    var page_obj = {page_number: 1, items_per_page: 4};

    function loadComments(page_number, items_per_page) {
        var commentsTreeApiUrl = 'comment/json/' + page_number + '/' + items_per_page;
        $.ajax({
            type: "GET",
            url: commentsTreeApiUrl,
            success: function (data) {
                parseJson(data);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.error("Status: " + textStatus);
                console.error("Error: " + errorThrown);
            }
        });
    }

    function parseJson(data) {
        var hasNextPage = data.page.has_next;
        var commentsTree = data.comments_list;
        var renderedTree = renderTree(commentsTree);
        $('.comments-wrapper').append(renderedTree);
        if (hasNextPage) {
            page_obj.page_number += 1;
        }
    }

    function renderTree(commentsTree) {
        var html = [];
        $.each(commentsTree, function (index, comment) {
            html.push(headerTreeTemplate(comment));
            if (comment.children.length) {
                html.push(renderTree(comment.children));
            }

            html.push(footerTreeTemplate());
        });
        return html.join("").toString();
    }

    function headerTreeTemplate(comment) {
        var root_id = comment.root_id === undefined ? null : comment.root_id;
        var parent_id = comment.parent_id === undefined ? null : comment.parent_id;

        return [
            '<div id="comment-' + comment.id + '" class="comment comment-level-1">' +
            '<div class="comment-wrapper">' +
            '<div class="comment-header">' +
            '<img class="comment-header-avatar" ' +
            'src="http://www.gravatar.com/avatar/0641c4913a53a04c1af5ad5867a38488?s=35&d=mm">' +
            '<div class="comment-header-author">' +
            '<span class="comment-header-author-name">' + comment.user.full_name +
            '</span>:' +
            '</div>' +
            '<div class="comment-header-anchor">' +
            '<a class="comment-header-anchor-link" href="">' + comment.pub_date +
            '</a>' +
            '</div>' +
            '</div>' +
            '<div class="comment-content">' + comment.content +
            '</div>' +
            '<a href="" class="comment-reply-link" ' +
            'data-root-id="' + root_id + '" data-parent-id="' + parent_id + '">' +
            'Reply' +
            '</a>' +
            '</div>'
        ].toString();

    }

    function footerTreeTemplate() {
        return ['</div>'].toString();
    }

    // make call to load first comments
    loadComments(page_obj.page_number, page_obj.items_per_page);
});