import React from "react";
import { Form, Input, Button, Spin, Typography } from "antd";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const { Title } = Typography;

const formItemLayout = {
  labelCol: { span: 24 },
  wrapperCol: { span: 24 },
};

const buttonItemLayout = {
  wrapperCol: { span: 24, offset: 0 },
};

const RecommendationForm = () => {
  const [loading, setLoading] = React.useState(false);
  const navigate = useNavigate();

  // let recommendations = [
  //   {
  //     "Recommended Books - By Same Author": [
  //       {
  //         ISBN: "0140430423",
  //         Title: "Hard Times for These Times (English Library)",
  //         Author: "Charles Dickens",
  //         Year: 1985,
  //         Publisher: "Penguin Putnam~mass",
  //       },
  //       {
  //         ISBN: "0893753564",
  //         Title: "Christmas Carol",
  //         Author: "Charles Dickens",
  //         Year: 1980,
  //         Publisher: "Troll Communications",
  //       },
  //       {
  //         ISBN: "0812580036",
  //         Title: "Oliver Twist",
  //         Author: "Charles Dickens",
  //         Year: 1998,
  //         Publisher: "Tor Books",
  //       },
  //       {
  //         ISBN: "1853262447",
  //         Title: "Old Curiosity Shop (Wordsworth Collection)",
  //         Author: "Charles Dickens",
  //         Year: 1998,
  //         Publisher: "Wordsworth Editions Ltd",
  //       },
  //       {
  //         ISBN: "1853262447",
  //         Title: "Old Curiosity Shop (Wordsworth Collection)",
  //         Author: "Charles Dickens",
  //         Year: 1998,
  //         Publisher: "Wordsworth Editions Ltd",
  //       },
  //     ],
  //   },
  //   {
  //     "Recommended Books - By Same Publisher": [
  //       {
  //         ISBN: "0451207521",
  //         Title: "Jackdaws",
  //         Author: "Ken Follett",
  //         Year: 2002,
  //         Publisher: "Signet Book",
  //       },
  //       {
  //         ISBN: "0451172817",
  //         Title: "Needful Things",
  //         Author: "Stephen King",
  //         Year: 2004,
  //         Publisher: "Signet Book",
  //       },
  //       {
  //         ISBN: "0451188462",
  //         Title: "Desperation",
  //         Author: "Stephen King",
  //         Year: 1997,
  //         Publisher: "Signet Book",
  //       },
  //       {
  //         ISBN: "0451172817",
  //         Title: "Needful Things",
  //         Author: "Stephen King",
  //         Year: 2004,
  //         Publisher: "Signet Book",
  //       },
  //       {
  //         ISBN: "0451172817",
  //         Title: "Needful Things",
  //         Author: "Stephen King",
  //         Year: 2004,
  //         Publisher: "Signet Book",
  //       },
  //     ],
  //   },
  //   {
  //     "Recommended Books. Collaborative": [
  //       {
  //         ISBN: "0718143515",
  //         Title: "Field of Thirteen",
  //         Author: "Dick Francis",
  //         Year: 2002,
  //         Publisher: "Penguin Putnam~trade",
  //       },
  //       {
  //         ISBN: "0345351738",
  //         Title: "2061: Odyssey Three",
  //         Author: "Arthur C. Clarke",
  //         Year: 1988,
  //         Publisher: "Ballantine Books",
  //       },
  //       {
  //         ISBN: "0142437204",
  //         Title: "Jane Eyre (Penguin Classics)",
  //         Author: "Charlotte Bronte",
  //         Year: 2003,
  //         Publisher: "Penguin Books",
  //       },
  //       {
  //         ISBN: "0380977273",
  //         Title: "Something Wicked This Way Comes",
  //         Author: "Ray Bradbury",
  //         Year: 1999,
  //         Publisher: "Eos",
  //       },
  //       {
  //         ISBN: "0140157379",
  //         Title: "Haroun and the Sea of Stories",
  //         Author: "Salman Rushdie",
  //         Year: 1991,
  //         Publisher: "Penguin Books",
  //       },
  //     ],
  //   },
  //   {
  //     "Recommended Books 2. Correlation Based": [
  //       {
  //         ISBN: "0787119784",
  //         Title:
  //           "Alice in Wonderland: Including Alice's Adventures in Wonderland and Through the Looking-Glass",
  //         Author: "Lewis Carroll",
  //         Year: 1999,
  //         Publisher: "Dove Books",
  //       },
  //       {
  //         ISBN: "0385721765",
  //         Title: "Swimming Toward the Ocean",
  //         Author: "Carole L. Glickfeld",
  //         Year: 2002,
  //         Publisher: "Anchor Books/Doubleday",
  //       },
  //       {
  //         ISBN: "0141304235",
  //         Title: "The Case of the Measled Cowboy (Hank the Cowdog, 33)",
  //         Author: "John R. Erickson",
  //         Year: 1999,
  //         Publisher: "Puffin Books",
  //       },
  //       {
  //         ISBN: "0140442618",
  //         Title: "Timaeus and Critias (Penguin Classics)",
  //         Author: "Plato",
  //         Year: 1972,
  //         Publisher: "Penguin Books",
  //       },
  //       {
  //         ISBN: "0451521897",
  //         Title: "Treasure Island",
  //         Author: "Robert Louis Stevenson",
  //         Year: 1994,
  //         Publisher: "Signet Classics",
  //       },
  //     ],
  //   },
  //   {
  //     "Recommended Books 3. Nearest Neighbours Based": [
  //       {
  //         ISBN: "0446611867",
  //         Title: "A Bend in the Road",
  //         Author: "Nicholas Sparks",
  //         Year: 2002,
  //         Publisher: "Warner Books",
  //       },
  //       {
  //         ISBN: "0802130208",
  //         Title: "A Confederacy of Dunces (Evergreen Book)",
  //         Author: "John Kennedy Toole",
  //         Year: 1987,
  //         Publisher: "Grove Press",
  //       },
  //       {
  //         ISBN: "0679772677",
  //         Title: "A Civil Action",
  //         Author: "JONATHAN HARR",
  //         Year: 1996,
  //         Publisher: "Vintage",
  //       },
  //       {
  //         ISBN: "0375725784",
  //         Title: "A Heartbreaking Work of Staggering Genius",
  //         Author: "Dave Eggers",
  //         Year: 2001,
  //         Publisher: "Vintage Books USA",
  //       },
  //       {
  //         ISBN: "0375702709",
  //         Title: "A Lesson Before Dying (Vintage Contemporaries (Paperback))",
  //         Author: "Ernest J. Gaines",
  //         Year: 1997,
  //         Publisher: "Vintage Books USA",
  //       },
  //     ],
  //   },
  //   {
  //     "Recommended Books 4. Content Based": [
  //       {
  //         ISBN: "0449212602",
  //         Title: "The Handmaid's Tale",
  //         Author: "Margaret Atwood",
  //         Year: 1989,
  //         Publisher: "Fawcett Books",
  //       },
  //       {
  //         ISBN: "0156001942",
  //         Title: "Winter's Tale",
  //         Author: "Mark Helprin",
  //         Year: 1995,
  //         Publisher: "Harvest Books",
  //       },
  //       {
  //         ISBN: "038549081X",
  //         Title: "The Handmaid's Tale : A Novel",
  //         Author: "Margaret Atwood",
  //         Year: 1998,
  //         Publisher: "Anchor",
  //       },
  //       {
  //         ISBN: "0515131083",
  //         Title: "Plantation: A Lowcountry Tale",
  //         Author: "Dorothea Benton Frank",
  //         Year: 2001,
  //         Publisher: "Jove Books",
  //       },
  //       {
  //         ISBN: "0679405283",
  //         Title: "The Tale of the Body Thief (Vampire Chronicles)",
  //         Author: "Anne Rice",
  //         Year: 1992,
  //         Publisher: "Alfred A. Knopf",
  //       },
  //     ],
  //   },
  //   {
  //     "Recommended Books 5. Hybrid Approach (Content+Collaborative) Using percentile":
  //       [
  //         {
  //           ISBN: "0718143515",
  //           Title: "Field of Thirteen",
  //           Author: "Dick Francis",
  //           Year: 2002,
  //           Publisher: "Penguin Putnam~trade",
  //         },
  //         {
  //           ISBN: "0345351738",
  //           Title: "2061: Odyssey Three",
  //           Author: "Arthur C. Clarke",
  //           Year: 1988,
  //           Publisher: "Ballantine Books",
  //         },
  //         {
  //           ISBN: "0142437204",
  //           Title: "Jane Eyre (Penguin Classics)",
  //           Author: "Charlotte Bronte",
  //           Year: 2003,
  //           Publisher: "Penguin Books",
  //         },
  //         {
  //           ISBN: "0380977273",
  //           Title: "Something Wicked This Way Comes",
  //           Author: "Ray Bradbury",
  //           Year: 1999,
  //           Publisher: "Eos",
  //         },
  //         {
  //           ISBN: "0140157379",
  //           Title: "Haroun and the Sea of Stories",
  //           Author: "Salman Rushdie",
  //           Year: 1991,
  //           Publisher: "Penguin Books",
  //         },
  //       ],
  //   },
  // ];

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/recommend", {
        isbn: values.isbn,
        bookName: values.bookName,
        number: values.number,
        place: values.place,
      });
      navigate("/recommendations", {
        state: { recommendations: response.data },
        // state: { recommendations: recommendations },
      });
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#121212", // Dark background color
        color: "#E0E0E0", // Light text color
      }}
    >
      <Form
        {...formItemLayout}
        // layout="vertical"
        onFinish={handleSubmit}
        initialValues={{
          isbn: "",
          bookName: "",
          number: "",
          place: "",
        }}
        style={{
          maxWidth: 600,
          width: "100%",
          padding: "20px",
          backgroundColor: "#1E1E1E", // Form background color
          borderRadius: "8px",
          boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
        }}
      >
        <Title style={{ color: "#FFFFFF" }}>Enter Book Details</Title>
        <Form.Item
          name="isbn"
          label={<span style={{ color: "#FFFFFF" }}>ISBN</span>}
            rules={[{ required: true, message: "Please input the ISBN!" }]}
        >
          <Input
            placeholder="Enter ISBN"
            style={{
              backgroundColor: "#2C2C2C",
              borderColor: "#3C3C3C",
              color: "#FFFFFF",
            }}
          />
        </Form.Item>
        <Form.Item
          name="bookName"
          label={<span style={{ color: "#FFFFFF" }}>Book Name</span>}
            rules={[{ required: true, message: "Please input the book name!" }]}
        >
          <Input
            placeholder="Enter Book Name"
            style={{
              backgroundColor: "#2C2C2C",
              borderColor: "#3C3C3C",
              color: "#FFFFFF",
            }}
          />
        </Form.Item>
        <Form.Item
          name="number"
          label={<span style={{ color: "#FFFFFF" }}>Number of Books</span>}
            rules={[
              { required: true, message: "Please input the number of books!" },
            ]}
        >
          <Input
            type="number"
            placeholder="Enter Number of Books"
            style={{
              backgroundColor: "#2C2C2C",
              borderColor: "#3C3C3C",
              color: "#FFFFFF",
            }}
          />
        </Form.Item>
        <Form.Item
          name="place"
          label={<span style={{ color: "#FFFFFF" }}>Place</span>}
            rules={[{ required: true, message: "Please input the place!" }]}
        >
          <Input
            placeholder="Enter Place"
            style={{
              backgroundColor: "#2C2C2C",
              borderColor: "#3C3C3C",
              color: "#FFFFFF",
            }}
          />
        </Form.Item>
        <Form.Item {...buttonItemLayout}>
          <Button
            type="primary"
            htmlType="submit"
            loading={loading}
            style={{
              backgroundColor: "#6200EE", // Primary button color
              color: "#FFFFFF",
              borderColor: "#6200EE",
            }}
          >
            Get Recommendations
          </Button>
        </Form.Item>
      </Form>
      {loading && (
        <Spin
          size="large"
          tip="Loading..."
          style={{ paddingTop: "50px", color: "#E0E0E0" }}
        />
      )}
    </div>
  );
};

export default RecommendationForm;
