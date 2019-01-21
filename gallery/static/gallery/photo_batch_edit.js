var photosInSameAlbums;
var photosInSameAlbums;

document.addEventListener('DOMContentLoaded', function() {
  // TODO XHR to get list of all albums
  albumsSelector = $("#select_albums");
  photosInSameAlbums = true;

  albumsSelector.prop("disabled", true);
  albumsSelector.blur();


  albumsSelector.change(function() {
    // If selected photos are from different albums, ask for confirmation before overriding albums.
    if(!photosInSameAlbums) {
      if(confirm("The selected photos are in different albums. Do you want to override this and put them in the selected albums instead?")) {
        photosInSameAlbums = true;
      } else {
        $(this).val($(this).data("current"));
        $(this).blur();
        return false;
      }
    }
    $(this).data("current", $(this).val());

    //var selectedPhotos = $("#id_photos_field option:selected");
    var selectedPhotos = $(".ui-selected > img");
    var selectedAlbums = $("#id_albums_field option:selected");

    // Apply album selection to selected photos.
    selectedPhotos.each(function() {
      $(this).attr("data-albums", "[" + albumsSelector.val() + "]");

      // Send AJAX album change request to server
      console.log("albums: " + albumsSelector.val());
      $.ajax({
        url: $(this).parent().attr("href"), // XXX
        type: "PATCH",
        contentType: "application/json",
        data: JSON.stringify({
          //TODO: TODO
          photo: $(this).attr("data-photo"),
          albums: albumsSelector.val()
        }),
        error: function(data) {
          alert("Could not change albums: " + data.statusText);
        }
      });
    });
  });
});

function openEditSidebar() {
  //$("#open-edit-sidebar-button").css("display", "none");
  $("#content").addClass("right-sidebar-shown");
  $("#gallery>a").addClass("disabled");

  $('#gallery').justifiedGallery({
    rowHeight: 120,
    margins: 12,
  }).selectable({
    stop: function() {
      //var selectedPhotos = $("#id_photos_field option:selected");
      var selectedPhotos = $(".ui-selected > img");

      if(selectedPhotos.length === 0) {
        albumsSelector.val([]);
        albumsSelector.prop("disabled", true);
        albumsSelector.blur();
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
    }
  });
}

function closeEditSidebar() {
  $("#content").removeClass("right-sidebar-shown");
  $("#gallery>a").removeClass("disabled");

  $('#gallery').justifiedGallery({
    rowHeight: jgRowHeight,
    margins: 3,
  }).selectable("destroy");
}
