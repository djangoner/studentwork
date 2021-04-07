var search_query = $("#documentTitle").attr('value')
var searchResults = $("#similarDocuments")

function search(query){
    $('.loading-indicator').removeClass('hide')
    searchResults.html('')

    $.ajax({
        url: "/search/results",
        data: {
            search: search_query,
            inline: true,
        }
    }).done(html => {
        console.log("Loaded!")
        $('.loading-indicator').addClass('hide')
        searchResults.html(html)
    }).fail((err) =>{
        console.log("Failed.")
        $('.loading-indicator').addClass('hide')
        $(".err-container").removeClass('hide')
        // searchResults.text(`Код: ${err.status}, ${err.statusText}`)
    })
}
search(search_query)