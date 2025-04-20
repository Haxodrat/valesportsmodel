// imports
import React from 'react';
import { Link } from 'react-router-dom';
import './App.css';

const Contact = () => (
  <div className="contact-page">
    <h2>Contact Us</h2>
    <form>
      <div>
        <label>Name</label>
        <input type="text" />
      </div>
      <div>
        <label>Email</label>
        <input type="email" />
      </div>
      <div>
        <label>Message</label>
        <textarea />
      </div>
      <button type="submit">Send Message</button>
    </form>
    <Link to="/" className="back-home">← Back to Home</Link>
  </div>
);

export default Contact;
