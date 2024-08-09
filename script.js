function getParameterByName(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

document.addEventListener("DOMContentLoaded", () => {
    const ogImage = document.getElementById("og-image");
    const ogVideoUrl = document.getElementById("og-video-url");
    const ogVideoWidth = document.getElementById("og-video-width");
    const ogVideoHeight = document.getElementById("og-video-height");
    const errorMessage = document.getElementById("error-message");

    const url = getParameterByName('url');
    const thumbnail = getParameterByName('thumbnail') || 'https://cdn.pixabay.com/photo/2013/07/13/11/45/play-158609_1280.png';
    const width = getParameterByName('width') || '';
    const height = getParameterByName('height') || '';

    if (url) {
        ogImage.content = thumbnail;
        ogVideoUrl.content = url;
        ogVideoWidth.content = width;
        ogVideoHeight.content = height;
    } else {
        errorMessage.classList.remove('hidden');
    }
});
