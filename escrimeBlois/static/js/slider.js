function slider() {
  $(".menu-recherche").toggle("slide");
  $("#btn-entrant").removeClass("hidden");
}
function sliderEntrant() {
  $("#btn-entrant").addClass("hidden");
  $(".menu-recherche").toggle("slide");
}
