// src/Contact.tsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Contact() {
  const [name, setName]   = useState('');
  const [email, setEmail] = useState('');
  const [msg, setMsg]     = useState('');
  const [sent, setSent]   = useState(false);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: POST to your backend
    setSent(true);
  };

  if (sent) {
    return (
      <div className="max-w-lg mx-auto mt-12 p-8 bg-white rounded-lg shadow-lg text-center">
        <h2 className="text-2xl font-semibold mb-4">Thank you!</h2>
        <p>We’ve received your message and will get back to you soon.</p>
        <Link to="/" className="view-link mt-6 inline-block">
          ← Back to Home
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto mt-12 p-8 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-semibold mb-6 text-center">Contact Us</h2>
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 font-medium">Name</label>
          <input
            type="text" required
            value={name} onChange={e => setName(e.target.value)}
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring"
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Email</label>
          <input
            type="email" required
            value={email} onChange={e => setEmail(e.target.value)}
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring"
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">Message</label>
          <textarea
            required rows={5}
            value={msg} onChange={e => setMsg(e.target.value)}
            className="w-full border rounded px-3 py-2 focus:outline-none focus:ring"
          />
        </div>
        <button type="submit" className="view-link">
          Send Message
        </button>
        <div className="text-center mt-4">
          <Link to="/" className="text-gray-500 hover:underline">
            ← Back to Home
          </Link>
        </div>
      </form>
    </div>
  );
}
