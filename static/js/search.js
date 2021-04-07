var search_query = new URLSearchParams(location.search).get('search')
function search(query){
    $('.loading-indicator').removeClass('hide')
    $('.main-container .results').html('')

    $.ajax({
        url: "/search/results",
        data: {
            search: search_query,
        }
    }).done(html => {
        console.log("Loaded!")
        $('.loading-indicator').addClass('hide')
        $('.main-container .results').html(html)
    }).fail((err) =>{
        console.log("Failed.")
        $('.loading-indicator').addClass('hide')
        $(".err-container").removeClass('hide')
        $('.err-container .err-desc').text(`Код: ${err.status}, ${err.statusText}`)
    })
    // .always(e => {
    //     var search_forms = $(".results .search-form")
    //     search_forms.on('submit', e => {
    //         tx = $(e.target).find('input').val()

    //         search_forms.find("input").val(tx)
    //         console.log(tx)
    //         search_forms.off()
    //         search(tx)
    //         return false;
    //     })
    // })
    // app.search(search_query)
}
search(search_query)