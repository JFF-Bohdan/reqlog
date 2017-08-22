% rebase("logged_in_base.tpl", title="Page Title")



<div class="box box-primary">
  <div class="box-header with-border">
    <h3 class="box-title">General information</h3>
  <div>
	<small>Added at {{node.adding_dts.date().isoformat()}} updated at {{node.update_dts.date().isoformat()}} [id={{node.dcn_id}}]</small>
  </div>
  </div>
  <!-- /.box-header -->
  <!-- form start -->
  <form role="form" action="/settings/node/{{node.dcn_uid}}" method="post">
    <div class="box-body">
  
      <div class="form-group">
        <label for="nodeName">Node name</label>
        <input type="text" class="form-control" name="node_name" id="nodeName" placeholder="Enter node name" value="{{node.dcn_name}}">
      </div>
	
      <div class="form-group">
        <label for="nodeUid">Node uid</label>
        <input type="text" class="form-control" name="node_uid" id="nodeUid" placeholder="Please, click button to generate new UID" value="{{node.dcn_uid}}" disabled>
      </div>				
	
      <div class="form-group">
        <label>Description</label>
        <textarea name="node_description" class="form-control" rows="3" placeholder="Enter...">{{node.description}}</textarea>
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
</script>