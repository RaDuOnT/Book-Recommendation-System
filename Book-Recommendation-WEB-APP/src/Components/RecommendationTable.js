import React, { useEffect, useState } from "react";
import { Carousel, Card, Tabs, Button, Dropdown, Menu } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import { EllipsisOutlined } from "@ant-design/icons";
import "./RecommendationTable.css";

const RecommendationTable = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [bookDetails, setBookDetails] = useState({});

  const goBackHome = () => {
    navigate("/"); // Navigates back to the home page
  };

  // Initialize book details from the passed state
  useEffect(() => {
    if (location.state && location.state.recommendations) {
      const recommendations = location.state.recommendations;
      const newBookDetails = {};
      recommendations.forEach((categoryData) => {
        const category = Object.keys(categoryData)[0];
        const books = categoryData[category].map((book) => ({
          ...book,
          coverImage:
            localStorage.getItem(book.ISBN) || "/path/to/image-not-found.jpg",
        }));
        newBookDetails[category] = books;
      });
      setBookDetails(newBookDetails);
    }
  }, [location.state]);

  useEffect(() => {
    const fetchCoverImages = async () => {
      const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      for (let category in bookDetails) {
        for (let book of bookDetails[category]) {
          const cachedCover = localStorage.getItem(book.ISBN);
          if (!cachedCover) {
            try {
              const response = await fetch(
                `https://covers.openlibrary.org/b/isbn/${book.ISBN}-M.jpg?default=false`
              );
              if (response.ok) {
                const imageUrl = response.url;
                localStorage.setItem(book.ISBN, imageUrl);
                updateCoverImage(book.ISBN, imageUrl);
              } else {
                localStorage.setItem(book.ISBN, "/path/to/image-not-found.jpg");
                updateCoverImage(book.ISBN, "/path/to/image-not-found.jpg");
              }
            } catch (error) {
              console.log(error.message);
              localStorage.setItem(book.ISBN, "/path/to/image-not-found.jpg");
              updateCoverImage(book.ISBN, "/path/to/image-not-found.jpg");
            }
            // Implement delay between requests to respect rate limiting
            await delay(3000); // Delay for 3 seconds
          } else {
            updateCoverImage(book.ISBN, cachedCover);
          }
        }
      }
    };

    fetchCoverImages();
  }, [bookDetails]);

  const updateCoverImage = (isbn, url) => {
    const updatedBookDetails = { ...bookDetails };
    for (let category in updatedBookDetails) {
      updatedBookDetails[category] = updatedBookDetails[category].map((book) =>
        book.ISBN === isbn ? { ...book, coverImage: url } : book
      );
    }
    setBookDetails(updatedBookDetails);
  };

  const tabItems = Object.entries(bookDetails).map(([category, books]) => ({
    label: <span style={{ color: "#FFFFFF" }}>{category}</span>,
    key: category,
    children: (
      <Carousel dots={{ className: "custom-dot-class" }} arrows>
        {books.map((book, index) => (
          <Card
            className="custom-card"
            key={index}
            title={
              <div style={{ textAlign: "center", color: "#FFFFFF" }}>
                {book.Title}
              </div>
            }
            style={{
              width: 300,
              margin: "0 auto",
              textAlign: "center",
              backgroundColor: "#2E2E2E", // Darker card background
              color: "#FFFFFF", // Light card text
              border: "1px solid #333333",
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                textAlign: "center",
                padding: "20px",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "300px",
                  overflow: "hidden",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  // backgroundColor: "#000000", // Background color for image container
                  borderRadius: "4px",
                  marginBottom: "10px",
                }}
              >
                <img
                  src={book.coverImage || "/path/to/image-not-found.jpg"}
                  alt={`Cover of ${book.Title}`}
                  style={{
                    maxWidth: "100%",
                    maxHeight: "100%",
                    objectFit: "contain", // Ensures the image covers the div area
                  }}
                />
              </div>
              <p style={{ color: "#FFFFFF", margin: "5px 0" }}>
                ISBN: {book.ISBN}
              </p>
              <p style={{ color: "#FFFFFF", margin: "5px 0" }}>
                Author: {book.Author}
              </p>
              <p style={{ color: "#FFFFFF", margin: "5px 0" }}>
                Year: {book.Year}
              </p>
              <p style={{ color: "#FFFFFF", margin: "5px 0" }}>
                Publisher: {book.Publisher}
              </p>
            </div>
          </Card>
        ))}
      </Carousel>
    ),
  }));

  const renderTabBar = (props, DefaultTabBar) => {
    const { panes } = props;
    const visibleTabs = panes.slice(0, 4);
    const dropdownTabs = panes.slice(4);

    return (
      <div className="custom-tab-bar">
        <DefaultTabBar {...props} panes={visibleTabs} />
        {dropdownTabs.length > 0 && (
          <Dropdown
            menu={{
              items: dropdownTabs.map((pane) => ({
                key: pane.key,
                label: pane.props.tab,
                onClick: () => props.onChange(pane.key),
              })),
            }}
            trigger={["click"]}
          >
            <Button shape="circle" icon={<EllipsisOutlined />} />
          </Dropdown>
        )}
      </div>
    );
  };

  return (
    <div
      style={{
        height: "100vh",
        width: "100vw", // Make the container full width
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#121212", // Main dark background
      }}
    >
      <div
        style={{
          width: "100%", // Make the container full width
          margin: "0 auto",
          backgroundColor: "#1E1E1E", // Container dark background
          borderRadius: "8px",
          boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
          overflow: "hidden", // Ensure content doesn't overflow
        }}
      >
        <div className="tabs-container">
          <Tabs
            type="card"
            centered
            defaultActiveKey="1"
            renderTabBar={renderTabBar} // Custom tab bar renderer
            items={tabItems}
            tabBarStyle={{
              backgroundColor: "#333333", // Tab bar background
              color: "#FFFFFF", // Tab bar text color
              display: "flex",
              justifyContent: "center",
              flexWrap: "nowrap", // Prevent wrapping of tabs
            }}
          />
        </div>
      </div>
      <Button
        type="primary"
        onClick={goBackHome}
        style={{
          marginTop: "20px",
          backgroundColor: "#6200EE", // Vibrant button color
          color: "#FFFFFF",
          borderColor: "#6200EE",
        }}
      >
        Back to Home
      </Button>
    </div>
  );
};

export default RecommendationTable;
