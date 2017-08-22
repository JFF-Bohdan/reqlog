% rebase("logged_in_base.tpl", title="Page Title")

<div class="box">
  <div class="box-header with-border">
    <h3 class="box-title">General information</h3>
  </div>
  <div class="box-body">
	<div class="box-body">
      <dl class="dl-horizontal">
        <dt>Name</dt>
        <dd>{{device.dcd_name}}</dd>
		
        <dt>UID</dt>
        <dd><tt>{{device.dcd_uid}}</tt></dd>
		
		<dt>Write token</dt>
		<dd>
		  <tt>{{device.write_token if device.write_token else "<not specified>"}}</tt>
		</dd>

		<dt>Read token</dt>
		<dd>
		  <tt>{{device.read_token if device.read_token else "<not specified>"}}</tt>
		</dd>		

        <dt>Last activity</dt>
        <dd>{{device.last_activity}}</dd>
		
		<dt>Description</dt>
        <dd>{{device.description}}</dd>
		
      </dl>
    </div>
  </div>
  <!-- /.box-body -->
  <div class="box-footer">
    <small>Added at {{device.adding_dts.date().isoformat()}} updated at {{device.update_dts.date().isoformat()}} (id={{device.dcd_id}})</small>
  </div>
  <!-- /.box-footer-->
</div>


<h4>Last requests (max. {{max_requests_count}})</h4>

  <!-- /.box-header -->
  <div class="box-body">
    <table id="example1" class="table table-bordered table-striped">
      <thead>
      <tr>
        <th>Request date</th>
        <th>Request uid</th>		
        <th>Method</th>
        <th>Params (max. {{max_params_count}})</th>
      </tr>
      </thead>
      <tbody>		
		% for request in device.requests:
			<tr>
			  <td><tt>{{request.adding_dts.isoformat()}}</tt></td>
			  <td>
				<tt>
					{{request.request_uid}}
				</tt>
			  </td>			  
			  <td>{{request.method}}</td>
			  <td>
			    <a href="/brief/device/{{device.dcd_uid}}/request/{{request.request_uid}}">Detailed</a>
			    <dl class="dl-horizontal">
					% for parameter in request.parameters:
						<dt>{{parameter.parameter_name}}</dt>
						<dd>{{parameter.parameter_value}}</dd>				
					% end
				</dl>				
			  </td>
			</tr>				
		% end	  

      </tbody>
    </table>
  </div>
  <!-- /.box-body -->