// Pagination
function navigateToPage(pageNumber) {
    const urlParams = new URLSearchParams(window.location.search);

    urlParams.set('page', pageNumber);

    window.location.href = `?${urlParams.toString()}`;
}