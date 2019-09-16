$('.delete').on('click', function() {
    var post_id = $(this).attr('id')
    if (confirm("Delete this post?")) {
        $.ajax({
            type: 'GET',
            url: `/delete/${post_id}`,
            context: this,
            success: function(result) {
                if (result.status === 1) {
                    $(this).closest("li").remove();
                }
            }
        });
    };
});