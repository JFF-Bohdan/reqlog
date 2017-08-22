% rebase("logged_in_base.tpl", title="Page Title")

<div class="box">
  <div class="box-header">
    <h3 class="box-title">Devices list</h3>
  </div>
  <!-- /.box-header -->
  <div class="box-body">
    <table id="example1" class="table table-bordered table-striped">
      <thead>
      <tr>
        <th>Name</th>
        <th>Uid</th>
        <th>Last activity timestamp</th>
		<th>Write token</th>
		<th>Node name</th>
      </tr>
      </thead>
      <tbody>
		% for device, node in data:
			<tr>
			  <td>
				<strong>
				  <a href="/settings/device/{{device.dcd_uid}}">
					{{device.dcd_name}} <small>(edit)</small>
				  </a>
				</strong>
			  </td>
			  <td>
				<tt>{{device.dcd_uid}}</tt>
			  </td>
			  <td>{{device.last_activity.isoformat() if device.last_activity else ""}}</td>
			  <td>
			    <tt>{{device.write_token}}</tt>
			  </td>
			  <td>{{node.dcn_name}}</td>
			</tr>				
		% end
      </tbody>
    </table>
  </div>
  <!-- /.box-body -->
</div>
