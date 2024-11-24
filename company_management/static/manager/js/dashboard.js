
$(document).ready(function () {
    fetchUserInfo();

    loadUserData();
  });

  function fetchUserInfo() {
    $.ajax({
      url: "/api/user-info/",
      type: "GET",
      dataType: "json",
      success: function (response) {
        $("#user-info").html(`
          <p><strong>Name:</strong> ${response.username}</p>
          <p><strong>Role:</strong> ${response.role}</p>
          <p><strong>Remaining Leave:</strong> ${response.remaining_leave}</p>
        `);
      },
      error: function () {
        $("#user-info").html("<p>Failed to load user information.</p>");
      },
    });
  }
  function loadUserData() {
    $.ajax({
      url: "/api/users/",
      type: "GET",
      dataType: "json",
      success: function (response) {
        const table = $('#usersTable').find('tbody');
        table.empty();

        response.forEach(user => {
          const row = `
            <tr>
              <td>${user.id}</td>
              <td>${user.user_name}</td>
              <td>${user.role}</td>
              <td>${user.remaining_leave}</td>
            </tr>
          `;
          table.append(row);
        });
      },
      error: function () {
        $("#message").html("<p>Failed to load users.</p>");
      }
    });
  }