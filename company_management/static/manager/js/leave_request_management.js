const fetchLeaveRequests = () => {
  $.ajax({
    url: "/api/leave-requests/",
    type: "GET",
    success: function (response) {
      $("#pending-requests, #approved-requests, #rejected-requests").empty();

      response.pending.forEach((request) => {
        $("#pending-requests").append(`
                    <tr>
                        <td>${request.id}</td>
                        <td>${request.user__username}</td>
                        <td>${request.start_date}</td>
                        <td>${request.end_date}</td>
                        <td>
                            <button class="btn btn-success btn-sm" onclick="handleRequest(${request.id}, 'approve')">Approve</button>
                            <button class="btn btn-danger btn-sm" onclick="handleRequest(${request.id}, 'reject')">Reject</button>
                        </td>
                    </tr>
                `);
      });

      response.approved.forEach((request) => {
        $("#approved-requests").append(`
                    <tr>
                        <td>${request.id}</td>
                        <td>${request.user__username}</td>
                        <td>${request.start_date}</td>
                        <td>${request.end_date}</td>
                    </tr>
                `);
      });

      response.rejected.forEach((request) => {
        $("#rejected-requests").append(`
                    <tr>
                        <td>${request.id}</td>
                        <td>${request.user__username}</td>
                        <td>${request.start_date}</td>
                        <td>${request.end_date}</td>
                    </tr>
                `);
      });
    },
    error: function () {
      alert("Failed to fetch leave requests.");
    },
  });
};

const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
const handleRequest = (id, action) => {
  $.ajax({
    url: `/api/manage-leave-request/${id}/`,
    type: "POST",
    contentType: "application/json",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
    },
    data: JSON.stringify({ action }),
    success: function (response) {
      alert(response.message);
      fetchLeaveRequests();
    },
    error: function () {
      alert("Failed to manage leave request.");
    },
  });
};

$(document).ready(function () {
  fetchLeaveRequests();
});
