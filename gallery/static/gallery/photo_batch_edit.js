var submitButton = $(":submit");
submitButton.prop("disabled", true); // wait until the user changed something

var photosSelector = $("#id_photos_field");
var albumsSelector = $("#id_albums_field");
albumsSelector.prop("disabled", true); // let user edit albums only when photos have been selected

var photosInSameAlbums = true;

photosSelector.change(function() {
  var selectedPhotos = $("#id_photos_field option:selected");

  if(selectedPhotos.length === 0) {
    albumsSelector.val([]);
    albumsSelector.prop("disabled", true);
    return;
  }
  albumsSelector.prop("disabled", false);

  // Check if all selected photos are in the same albums.
  photosInSameAlbums = true;
  var firstAlbumList;
  selectedPhotos.each(function(i, element) {
    var thisAlbumList = $(this).attr("data-albums"); // attr instead of data to avoid conversion to array
    if(i == 0) {
      firstAlbumList = thisAlbumList;
    }
    else {
      if(thisAlbumList !== firstAlbumList) {
        photosInSameAlbums = false;
        return false; // break
      }
    }
  });

  if(photosInSameAlbums) {
    // Select the (equal) albums of selected photos in the album picker.
    albumsSelector.val(JSON.parse(firstAlbumList));
  }
  else {
    albumsSelector.val([]);
  }
});

albumsSelector.change(function() {
  // If selected photos are from different albums, ask for confirmation before overriding albums.
  if(!photosInSameAlbums) {
    if(confirm("Really?")) {
      photosInSameAlbums = true;
    } else {
      $(this).val($(this).data("current"));
      $(this).blur();
      return false;
    }
  }
  $(this).data("current", $(this).val());

  var selectedPhotos = $("#id_photos_field option:selected");
  var selectedAlbums = $("#id_albums_field option:selected");

  // Apply album selection to selected photos.
  selectedPhotos.each(function() {
    $(this).attr("data-albums", "[" + albumsSelector.val() + "]");
  });

  // Enable submit button
  submitButton.prop("disabled", false);
});
