// Creates a new file and add it to our list
function ui_multi_add_file(id, file)
{
  var template = $('#files-template').text();
  template = template.replace('%%filename%%', file.name);

  template = $(template);
  template.prop('id', 'uploaderFile' + id);
  template.data('file-id', id);

  $('#files').find('li.empty').fadeOut(); // remove the 'no files yet'
  $('#files').prepend(template);
}

// Changes the status messages on our list
function ui_multi_update_file_status(id, status, message)
{
  $('#uploaderFile' + id).find('span').html(message).prop('class', 'status text-' + status);
}

// Updates a file progress, depending on the parameters it may animate it or change the color.
function ui_multi_update_file_progress(id, percent, color, active)
{
  color = (typeof color === 'undefined' ? false : color);
  active = (typeof active === 'undefined' ? true : active);

  var bar = $('#uploaderFile' + id).find('div.progress-bar');

  bar.width(percent + '%').attr('aria-valuenow', percent);
  bar.toggleClass('progress-bar-striped progress-bar-animated', active);

  if (percent === 0) {
    bar.html('');
  } else {
    bar.html(percent + '%');
  }

  if (color !== false) {
    bar.removeClass('bg-success bg-info bg-warning bg-danger');
    bar.addClass('bg-' + color);
  }
}

var error = function(message) {
  if ($("#bs-alert").length == 0) {
    $('body').append('<div class="modal fade" id="bs-alert" tabindex="-1">'+
      '<div class="modal-dialog">'+
      '<div class="modal-content">'+
      '<div class="modal-header">'+
      '<h2 class="modal-title">Error</h2>'+
      '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'+
      '</div>'+
      '<div class="modal-body">'+
      message+
      '</div>'+
      '<div class="modal-footer">'+
      '<button type="button" class="btn btn-default" data-dismiss="modal">Ok</button>'+
      '</div>'+
      '</div>'+
      '</div>'+
      '</div>')
  } else {
    $("#bs-alert .modal-body").text(message);
  }    
  $("#bs-alert").modal();
}


$(function() {
  $('#drag-and-drop-zone').dmUploader({
    url: photoUploadUrl,
    fieldName: 'file_field',
    maxFileSize: 50000000, // 50 MB
    allowedTypes: 'image/*',
    extFilter: ["jpg", "jpeg","png","gif"],
    onDragEnter: function() {
      // Happens when dragging something over the DnD area
      this.addClass('active');
    },
    onDragLeave: function() {
      // Happens when dragging something OUT of the DnD area
      this.removeClass('active');
    },
    onComplete: function() {
      // All files in the queue are processed (success or error)
      console.log('All pending tranfers finished');
    },
    onNewFile: function(id, file) {
      // When a new file is added using the file selector or the DnD area
      console.log('New file added #' + id);
      ui_multi_add_file(id, file);
    },
    onBeforeUpload: function(id) {
      // about tho start uploading a file
      console.log('Starting the upload of #' + id);
      ui_multi_update_file_status(id, 'uploading', 'Uploading...');
      ui_multi_update_file_progress(id, 0, '', true);
    },
    onUploadCanceled: function(id) {
      // Happens when a file is directly canceled by the user.
      ui_multi_update_file_status(id, 'warning', 'Canceled by User');
      ui_multi_update_file_progress(id, 0, 'warning', false);
    },
    onUploadProgress: function(id, percent) {
      // Updating file progress
      ui_multi_update_file_progress(id, percent);
    },
    onUploadSuccess: function(id, data) {
      // A file was successfully uploaded
      console.log('Server response for file #' + id + ': ' + JSON.stringify(data));
      console.log('Upload of file #' + id + ' COMPLETED');
      ui_multi_update_file_status(id, 'success', 'Done');
      ui_multi_update_file_progress(id, 100, 'success', false);
      // If the upload dialog is closed, we want to refresh
      $('#upload-modal').on('hidden.bs.modal', function(e) {
        location.reload(true);
      });
    },
    onUploadError: function(id, xhr, status, message) {
      ui_multi_update_file_status(id, 'danger', message);
      ui_multi_update_file_progress(id, 0, 'danger', false);
    },
    onFallbackMode: function() {
      console.log('Fallback mode');
    },
    onFileSizeError: function(file) {
      error('File \'' + file.name + '\' exceeds file size limit');
    },
    onFileTypeError: function(file) {
      error('File \'' + file.name + '\' is not an image');
    },
    onFileExtError: function(file) {
      error('File \'' + file.name + '\' has no known image filename extension');
    }
  });
});
