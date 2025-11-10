import React, { useEffect, useState } from "react";

const api = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({
    sku: "",
    model: "",
    brand: "",
    price: 0,
    quantity: 0,
  });

  const loadItems = async () => {
    const res = await fetch(`${api}/items`);
    setItems(await res.json());
  };

  useEffect(() => {
    loadItems();
  }, []);

  const add = async () => {
    await fetch(`${api}/items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    await loadItems();
  };

  const remove = async (id) => {
    await fetch(`${api}/items/${id}`, { method: "DELETE" });
    await loadItems();
  };

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>Refurbished Laptop Inventory</h1>

      <div style={{ display: "flex", gap: "5px", marginBottom: "10px" }}>
        <input placeholder="SKU" onChange={e=>setForm({...form, sku:e.target.value})}/>
        <input placeholder="Model" onChange={e=>setForm({...form, model:e.target.value})}/>
        <input placeholder="Brand" onChange={e=>setForm({...form, brand:e.target.value})}/>
        <input type="number" placeholder="Price" onChange={e=>setForm({...form, price:parseFloat(e.target.value)||0})}/>
        <input type="number" placeholder="Qty" onChange={e=>setForm({...form, quantity:parseInt(e.target.value)||0})}/>
        <button onClick={add}>Add</button>
      </div>

      <table border="1" cellPadding="8">
        <thead>
          <tr><th>SKU</th><th>Brand</th><th>Model</th><th>Price</th><th>Qty</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {items.map(it => (
            <tr key={it.id}>
              <td>{it.sku}</td>
              <td>{it.brand}</td>
              <td>{it.model}</td>
              <td>${it.price}</td>
              <td>{it.quantity}</td>
              <td><button onClick={() => remove(it.id)}>🗑️ Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
