% rebase("logged_in_base.tpl", title="Page Title")

<div class="box">
  <div class="box-header">
    <h3 class="box-title">Nodes list</h3>
  </div>
  <!-- /.box-header -->
  <div class="box-body">
    <table id="example1" class="table table-bordered table-striped">
      <thead>
      <tr>
        <th>Name</th>
        <th>Uid</th>
        <th>Last activity timestamp</th>
        <th>Devices</th>
      </tr>
      </thead>
      <tbody>
	% for node in nodes:
		<tr>
		  <td>
		    <strong>
			  <a href="/brief/node/{{node.dcn_uid}}">
			    {{node.dcn_name}}
			  </a>
			</strong>
		  </td>
		  <td><tt>{{node.dcn_uid}}</tt></td>
		  <td>{{node.last_activity_dts.isoformat() if node.last_activity_dts else ""}}</td>
		  <td>
		    <ul>
			  % for device in node.devices:
			    <li>
				  <a href="/brief/device/{{device.dcd_uid}}">
				    {{device.dcd_name}} (<tt>{{device.dcd_uid}}</tt>)
				  </a>
				</li>
			  % end
			<ul>
		  
		  </td>
		</tr>				
	% end
      </tbody>
    </table>
  </div>
  <!-- /.box-body -->
</div>
