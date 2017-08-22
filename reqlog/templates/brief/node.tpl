% rebase("logged_in_base.tpl", title="Page Title")

<div class="box">
  <div class="box-header with-border">
    <h3 class="box-title">General information</h3>
  </div>
  <div class="box-body">
	<div class="box-body">
      <dl class="dl-horizontal">
        <dt>Name</dt>
        <dd>{{node.dcn_name}}</dd>
		
        <dt>UID</dt>
        <dd><tt>{{node.dcn_uid}}</tt></dd>

        <dt>Last activity</dt>
        <dd>{{node.last_activity_dts}}</dd>
		
		<dt>Description</dt>
        <dd>{{node.description}}</dd>
		
      </dl>
    </div>
  </div>
  <!-- /.box-body -->
  <div class="box-footer">
    <small>Added at {{node.adding_dts.date().isoformat()}} updated at {{node.update_dts.date().isoformat()}} (id={{node.dcn_id}})</small>
  </div>
  <!-- /.box-footer-->
</div>

<h4>Devices</h4>

% for device in node.devices:
  
	<div class="box">
	  <div class="box-header with-border">
		<h3 class="box-title">{{device.dcd_name}}</h3>
	  </div>
	  <div class="box-body">
		<div class="box-body">

		      <dl class="dl-horizontal">
				<dt>Name</dt>
				<dd>
				  <a href="/brief/device/{{device.dcd_uid}}">
				    <strong>{{device.dcd_name}}</strong>
				  </a>
				</dd>
				
				<dt>UID</dt>
				<dd>
				  <a href="/brief/device/{{device.dcd_uid}}">
				    <tt>{{device.dcd_uid}}</tt>
				  </a>
				</dd>

				<dt>Last activity</dt>
				<dd>{{device.last_activity}}</dd>

				<dt>Write token</dt>
				<dd>
				  <tt>{{device.write_token if device.write_token else "<not specified>"}}</tt>
				</dd>

				<dt>Read token</dt>
				<dd>
				  <tt>{{device.read_token if device.read_token else "<not specified>"}}</tt>
				</dd>
				
				<dt>Description</dt>
				<dd>{{device.description}}</dd>
				
			  </dl>
		</div>
	  </div>
	  <!-- /.box-body -->
	  <div class="box-footer">
		<small>Added at {{node.adding_dts.date().isoformat()}} updated at {{node.update_dts.date().isoformat()}} (id={{device.dcd_id}})</small>
	  </div>
	  <!-- /.box-footer-->
	</div>		  
  
% end
