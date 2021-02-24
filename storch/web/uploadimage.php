<!doctype html>
<html>
 <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="description" content="$1">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet" type="text/css" href="style.css">

    <title>Upload Image</title>

    <?php    
    include_once 'dbConfig.php';
    ?>

</head>
<body>
     <?php
    if(isset($_POST['frameid'])){
        $sql = "INSERT INTO frames (idframes, time, thumbnail) VALUES (?,?,?)";
        
        if (!($stmt = $conn->prepare($sql))) {
            echo "Prepare failed: (" . $conn->errno . ") " . $conn->error;
        }        
        else if (!$stmt->bind_param("iss",$_POST['frameid'], $_POST['timestamp'], $_POST['thumbnail'])) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        else if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        }
        else {
            echo "<p>Success</p>";
        }
    }
    else {
        echo "<p>Failure</p>";        
    }
    $stmt->close();
    $conn->close();
    ?>

</body>
</html>