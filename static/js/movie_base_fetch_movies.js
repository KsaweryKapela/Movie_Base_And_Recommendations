//async function fetchMovies(hits, rotten, liked, new_, certified) {
//    response = await fetch('fetch_moviebase' + '?' + new URLSearchParams(
//    {'index': movie_index,
//    'hits': hits,
//    'key': userData,
//    'rotten': rotten,
//    'liked': liked,
//    'new': new_,
//    'certified': certified,
//    'search': search,
//    'key': inputBox.value
//    }));
//    const raw_data = await response.json();
//    return raw_data;
//}
//

order = ''
genres = []
rating = []
critics = []
audience = []


async function loadMovies() {

    placeArrows();

    const url_list = await fetchMovieBase();
    inputBox.setAttribute('value', url_list['key']);
    recognizeIconState(url_list);

    for (x = 0; x < 4; x++) {

        if (url_list['movie_url'][x] == undefined){
        cardButtons[x].style.visibility = "hidden";
        rightArrow.style.visibility = "hidden";
        img[x].style.visibility = "hidden";

        }else{
        rightArrow.style.visibility = "visible";
        cardButtons[x].style.visibility = "visible";
        printCard(x, url_list)}

        if (url_list['movie_url'][4] == undefined)
        {rightArrow.style.visibility = "hidden";}}}



async function fetchMovieBase() {
    response = await fetch('fetch_moviebase' + '?' + new URLSearchParams(
    {'index': movie_index,
     'key': inputBox.value,
    'order': order,

    'genres': genres,
    'rating': rating,
    'critics': critics,
    'audience': audience,

    }));
    const raw_data = await response.json();
    return raw_data;
}