% rebase("logged_in_base.tpl", title="Page Title")

<div class="box box-primary">
  <div class="box-header with-border">
    <h3 class="box-title">General information</h3>
  <div>
	<small>Added at {{device.adding_dts.date().isoformat()}} updated at {{device.update_dts.date().isoformat()}} [id={{device.dcd_id}}]</small>
  </div>
  </div>
  <!-- /.box-header -->
  <!-- form start -->
  <form role="form" action="/settings/device/{{device.dcd_uid}}" method="post">
    <div class="box-body">
  
      <div class="form-group">
        <label for="deviceName">Device name</label>
        <input type="text" class="form-control" name="device_name" id="deviceName" placeholder="Enter device name" value="{{device.dcd_name}}">
      </div>
	  
      <div class="form-group">
        <label for="nodeName">Node name</label>
        <input type="text" class="form-control" name="node_name" id="nodeName" placeholder="Enter device name" value="{{node.dcn_name}}" readonly>
      </div>	  
	
      <div class="form-group">
        <label for="deviceUid">Device uid</label>
        <input type="text" class="form-control" name="device_uid" style="font-family:monospace;" id="deviceUid" placeholder="Please, click button to generate new UID" value="{{device.dcd_uid}}" readonly>
      </div>
	  
      <div class="form-group">
        <label for="writeToken">Write token</label>
        <input type="text" class="form-control" style="font-family:monospace;" name="write_token" id="writeToken" placeholder="<not specified>" value="{{device.write_token if device.write_token else "<not specified>"}}" readonly>
		<a href="#" id="generate_new_write_token">Generate new</a>
		<a href="#" id="remove_write_token">Clear</a>
      </div>	  
	  
      <div class="form-group">
        <label for="readToken">Read token</label>
        <input type="text" class="form-control" name="read_token" style="font-family:monospace;" id="readToken" placeholder="<not specified>" value="{{device.read_token if device.read_token else "<not specified>"}}" readonly>
		<a href="#" id="generate_new_read_token">Generate new</a>
		<a href="#" id="remove_read_token">Clear</a>
      </div>
	  
      <div class="form-group">
        <label for="lastActivity">Last activity</label>
        <input type="text" class="form-control" name="last_activity" id="lastActivity" placeholder="Please, click button to generate new UID" value="{{device.last_activity if device.last_activity else "<not specified>"}}" readonly>
      </div>	  
	
      <div class="form-group">
        <label>Description</label>
        <textarea name="device_description" class="form-control" rows="3" placeholder="Enter...">{{device.description}}</textarea>
      </div>				

    </div>
    <!-- /.box-body -->
  
  <!-- /.box-body -->
  <div class="box-footer">
    <button type="submit" class="btn btn-primary">Submit</button>
	<button id="button_cancel" type="button" class="btn btn-default btn-cancel">Cancel</button>
  </div>			  
  </form>
</div>

<script>
	$( "#button_cancel" ).click(function() {
	  window.location.replace("/settings/devices");
	});

    // write token
	$( "#generate_new_write_token" ).click(function() {
	    var posting = $.post("/api/settings/device/{{device.dcd_uid}}/tokens/write/generate_new", { foo: "bar" } );
		posting.done(function( data ) {
		    $("#writeToken").val(data.new_uid);
			$("#writeToken").closest("div").addClass("has-success");
		});			
	});

	$( "#remove_write_token" ).click(function() {
	    var posting = $.post("/api/settings/device/{{device.dcd_uid}}/tokens/write/clear", { foo: "bar" } );
		posting.done(function( data ) {
		    $("#writeToken").val(data.new_uid);
			$("#writeToken").closest("div").addClass("has-success");
		});
	});

	// read token
	$( "#generate_new_read_token" ).click(function() {
	    var posting = $.post("/api/settings/device/{{device.dcd_uid}}/tokens/read/generate_new", { foo: "bar" } );
		posting.done(function( data ) {
		    $("#readToken").val(data.new_uid);
			$("#readToken").closest("div").addClass("has-success");
		});
	});

	$( "#remove_read_token" ).click(function() {
	    var posting = $.post("/api/settings/device/{{device.dcd_uid}}/tokens/read/clear", { foo: "bar" } );
		posting.done(function( data ) {
		    $("#readToken").val(data.new_uid);
			$("#readToken").closest("div").addClass("has-success");
		});
	});

	$(function(){
		$("[data-hide]").on("click", function(){
			$(this).closest("." + $(this).attr("data-hide")).addClass("hidden");
		});
	});	
	
</script>