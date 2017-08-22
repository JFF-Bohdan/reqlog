% rebase("logged_in_base.tpl", title="Page Title", add_datatables=True)
          <div class="box">
            <div class="box-header">
              <h3 class="box-title">Data Table With Full Features</h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="requests_datatable" class="table table-bordered table-striped">
                <thead>
                <tr>
                  <th>Added at</th>
                  <th>UID</th>
				  <th>Device name</th>
				  <th>Node name</th>
                  <th>Method</th>
				  <th>Params count</th>
				  <th>Actions</th>
                </tr>
                </thead>
                <tbody>
                </tbody>
                <tfoot>
                <tr>
                  <th>Added at</th>
                  <th>UID</th>
				  <th>Device name</th>
				  <th>Node name</th>
                  <th>Method</th>
                  <th>Params count</th>
				  <th>Actions</th>
                </tr>
                </tfoot>
              </table>
            </div>
            <!-- /.box-body -->
          </div>

		  
<script>
  $(function () {
	$('#requests_datatable').DataTable( {
		serverSide: true,
		ajax: {
			url: '/api/reports/all_requests/datatable',
			type: 'POST'
		},
		columns: [
			{ data: 'added_at' },
			{ data: 'uid' },
			{ data: 'dcd_name' },			
			{ data: 'dcn_name' },
			{ data: 'method' },
			{ data: 'params_count' },
			{ data: 'event_details_href_data'}
			
		],
		columnDefs: [
            {
                render: function ( data, type, row ) {
					if(type === 'display'){
					    return "<tt>" + data + "</tt>";
					} else {
						return data;
					}
                },
                targets: 1
            },
			{
                render: function ( data, type, row ) {
					if(type === 'display'){
					    return "<a href='/reports/device/" + data.dcd_uid + "/request/"+ data.event_uid +"/view_details'> View </a>&nbsp;&nbsp;" +
						"<a class='delete_event' href='/reports/device/" + data.dcd_uid + "/request/"+ data.event_uid +"/delete'> Delete </a>&nbsp;&nbsp;";
					} else {
						return data;
					}
                },			
				targets: -1,
				defaultContent: "<a href='#'>View</a>&nbsp;&nbsp;&nbsp;<button>Delete</button>"
			}			
        ],		

		deferRender: true,
		responsive: true,
        rowReorder: {
            selector: 'td:nth-child(2)'
        },
		searchDelay: 500
	} );	
	
  });
</script>