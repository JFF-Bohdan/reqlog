% rebase("logged_in_base.tpl", title="Page Title")


<div class="box">
  <div class="box-header with-border">
    <h3 class="box-title">General information</h3>
  </div>
  <div class="box-body">
	<div class="box-body">
      <dl class="dl-horizontal">
        <dt>UID</dt>
        <dd><tt>{{request.request_uid}}</tt></dd>
		
        <dt>Registered at</dt>
        <dd>{{request.adding_dts}}</dd>
		
		<dt>Method</dt>
		<dd>
		  {{request.method}}
		</dd>
		
		<dt>Node name</dt>
		<dd>
		  {{node.dcn_name}}
		</dd>		
		
		<dt>Node UID</dt>
		<dd>
		  <tt>{{node.dcn_uid}}</tt>
		</dd>				
		
		<dt>Device Name</dt>
		<dd>
		  {{device.dcd_name}}
		</dd>		
		<dt>Device UID</dt>
		<dd>
		  <tt>{{device.dcd_uid}}</tt>
		</dd>		

      </dl>
    </div>
  </div>
</div>


<div class="box">
  <div class="box-header with-border">
    <h3 class="box-title">Parameters</h3>
  </div>
  <div class="box-body">
	<div class="box-body">
      <dl class="dl-horizontal">
					% for parameter in parameters:
						<dt>{{parameter.parameter_name}}</dt>
						<dd>{{parameter.parameter_value}}</dd>				
					% end
      </dl>
    </div>
  </div>
  <!-- /.box-body -->
  <div class="box-footer">
    <small>Total count {{len(parameters)}}</small>
  </div>
  <!-- /.box-footer-->
</div>