async function generate() {
  const theme = document.getElementById('theme').value;
  const res = await fetch(`http://127.0.0.1:8000/generate?theme=${theme}`);
  const data = await res.json();
// build grid
  const table = document.getElementById('grid');
  table.innerHTML = '';
  data.grid.forEach((row, index) => {
    const tr_title = document.createElement('tr');
    const tr = document.createElement('tr');

    row.forEach((cell, cell_index) => {
      if(index == 0) {
        if (cell_index == 0) {
           const td_empty = document.createElement('td');
           td_empty.textContent = '';
           tr_title.appendChild(td_empty);
        }
        const td_title = document.createElement('td');
        td_title.textContent = cell_index;
        tr_title.appendChild(td_title);
      }


      const td = document.createElement('td');
      if(cell_index == 0) {
          const td_title = document.createElement('td');
          td_title.textContent = index;
          tr.appendChild(td_title);
      }
      td.textContent = cell === ' ' ? '' : cell;
      tr.appendChild(td);
    });
    table.appendChild(tr_title);
    table.appendChild(tr);
  })

//  Show list of words
  const all_words = document.getElementById('words');
  words.innerHTML = '';
  word_list = '';
  data.words.forEach(row => {
     if (row.length > 1) {
        word_list += row + '<br>';
     }
  })
  words.innerHTML = word_list;
 }