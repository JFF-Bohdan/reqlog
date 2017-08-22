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
        <th>Devices count</th>
      </tr>
      </thead>
      <tbody>
		% for node in nodes:
			<tr>
			  <td>
				<strong>
				  <a href="/settings/node/{{node.dcn_uid}}">
					{{node.dcn_name}} <small>(edit)</small>
				  </a>
				</strong>
			  </td>
			  <td>
				<tt>{{node.dcn_uid}}</tt>
			  </td>
			  <td>{{node.last_activity_dts.isoformat() if node.last_activity_dts else ""}}</td>
			  <td>
				<ul>
				  {{node.devices_count}}
				<ul>
			  </td>
			</tr>				
		% end
      </tbody>
    </table>
  </div>
  <!-- /.box-body -->
</div>
