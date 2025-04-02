$(document).ready(function() {
  $("#search-form").submit(function(event) {
      event.preventDefault(); // デフォルトの送信を防ぐ

      $.ajax({
          url: "/api/sales/", // DRFのAPIエンドポイント
          type: "GET",
          data: $(this).serialize(),
          dataType: "json",
          success: function(data) {
              let resultsDiv = $("#results");
              resultsDiv.empty(); // 検索結果をクリア

              if (data.results.length > 0) {
                  let table = `<table border="1">
                      <tr>
                          <th>販売経路</th>
                          <th>商品</th>
                          <th>モデル</th>
                          <th>購入日</th>
                          <th>購入数</th>
                      </tr>`;

                  data.results.forEach(function(record) {
                      table += `<tr>
                          <td>${record.channel}</td>
                          <td>${record.product}</td>
                          <td>${record.model}</td>
                          <td>${record.purchase_date}</td>
                          <td>${record.quantity}</td>
                      </tr>`;
                  });

                  table += `</table>`;
                  resultsDiv.append(table);
              } else {
                  resultsDiv.append("<p>検索結果がありません</p>");
              }
          },
          error: function() {
              alert("検索に失敗しました。");
          }
      });
  });
});
