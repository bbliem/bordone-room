var photosInSameAlbums;

document.addEventListener("DOMContentLoaded", function() {
  // TODO XHR to get list of all albums
  albumsSelector = $("#select-albums");
  photosInSameAlbums = true;

  $(".selection-required").prop("disabled", true);
  $(".selection-required").blur();

  albumsSelector.on("changed.bs.select", function() {
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
      // Send AJAX album change request to server
      $.ajax({
        url: $(this).parent().attr("href"), // XXX
        type: "PATCH",
        contentType: "application/json",
        data: JSON.stringify({
          photo: $(this).attr("data-photo"),
          albums: albumsSelector.val()
        }),
        error: function(data) {
          alert("Could not change albums: " + data.statusText);
          updateAlbumsSelectorValue();
        },
        success: function(data) {
          $(this).attr("data-albums", "[" + albumsSelector.val() + "]");
        }
      });
    });
  });
});

function updateAlbumsSelectorValue() {
  // Check if all selected photos are in the same albums.
  photosInSameAlbums = true;
  var firstAlbumList;
  var selectedPhotos = $(".ui-selected > img");
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
    albumsSelector.selectpicker({title: "Select albums"});
  }
  else {
    albumsSelector.val([]);
    albumsSelector.selectpicker({title: "Photos in different albums"});
  }
  albumsSelector.selectpicker("refresh").selectpicker("render");
}

function openEditSidebar() {
  //$("#open-edit-sidebar-button").css("display", "none");
  $("#content").addClass("right-sidebar-shown");
  $("#gallery>a").addClass("disabled");

  $("#gallery").justifiedGallery({
    rowHeight: 120,
    margins: 12,
  }).selectable({
    stop: function() {
      //var selectedPhotos = $("#id_photos_field option:selected");
      var selectedPhotos = $(".ui-selected > img");

      if(selectedPhotos.length === 0) {
        $(".selection-required").prop("disabled", true);
        $(".selection-required").blur();
        albumsSelector.val([]);
        albumsSelector.selectpicker({title: "No photos selected"});
        albumsSelector.selectpicker("render")
        return;
      }
      $(".selection-required").prop("disabled", false);

      updateAlbumsSelectorValue();
    }
  });
}

function initAlbumsSelector() {
  albumsSelector = $("#select-albums");
  albumsSelector.selectpicker({title: "No photos selected"});
  albumsSelector.val([]);
  albumsSelector.selectpicker("render");
}

function closeEditSidebar() {
  initAlbumsSelector();
  $("#content").removeClass("right-sidebar-shown");
  $("#gallery>a").removeClass("disabled");

  $("#gallery").justifiedGallery({
    rowHeight: jgRowHeight,
    margins: 3,
  }).selectable("destroy");
}

function selectAllPhotos() {
  // https://stackoverflow.com/questions/3140017/how-to-programmatically-select-selectables-with-jquery-ui
  $("a.ui-selectee").addClass("ui-selecting");
  // trigger the mouse stop event (this will select all .ui-selecting elements, and deselect all .ui-unselecting elements)
  $("#gallery").data("ui-selectable")._mouseStop(null);
}

function deselectAllPhotos() {
  // https://stackoverflow.com/questions/3140017/how-to-programmatically-select-selectables-with-jquery-ui
  $("a.ui-selectee").removeClass("ui-selected").addClass("ui-unselecting");
  // trigger the mouse stop event (this will select all .ui-selecting elements, and deselect all .ui-unselecting elements)
  $("#gallery").data("ui-selectable")._mouseStop(null);
}

function deleteSelected() {
  var selectedPhotos = $(".ui-selected > img");
  selectedPhotos.each(function() {
    // Send AJAX delete request to server
    $.ajax({
      url: $(this).parent().attr("href"), // XXX
      type: "DELETE",
      contentType: "application/json",
      data: JSON.stringify({
        photo: $(this).attr("data-photo"),
      }),
      error: function(data) {
        alert('Could not delete photo: ' + data.statusText);
      },
      success: function(data) {
        location.reload(true);
      }
    });
  });
}
