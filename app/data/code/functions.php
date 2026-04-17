<?php
 
function calculateTradeFee(float $amount, float $feeRate): float {
    return round($amount * $feeRate, 2); // Rounds to 2 decimal places
}

function formatCurrency(float $amount, string $currencySymbol = '$'): string {
    return $currencySymbol . number_format($amount, 2); // Rounds to 2 decimal places
}

function uploadImageReducedSize($image, $uploaddir = null){
    $storage_system = \Config::get('filesystems.default');
    $new_width = '1000';
    $new_height = '1777';
    $mime = getimagesize($image);
    if ($mime['mime'] == 'image/png') {
        $src_img = @imagecreatefrompng($image);
    }
    if ($mime['mime'] == 'image/jpg' || $mime['mime'] == 'image/jpeg' || $mime['mime'] == 'image/pjpeg') {
        $src_img = @imagecreatefromjpeg($image);
    }

    /* Local storage system */
    if($storage_system == 'local'){
        $moveToDir = storage_path() . '/app/public/' . $uploaddir . '/';

        // Make folder creation with permision - VP - 24/01/2024
        if (!\File::isDirectory($moveToDir))
            \File::makeDirectory($moveToDir, 0775, true, true);
    }
    /* Local storage system */


    $extension =  $image->getClientOriginalExtension();
    if (($extension == 'jpeg' || $extension == 'jpg' || $extension == 'png')) {
        $extension = 'jpg';
    }

    $image_name = str_replace('.', '', microtime(true)) . "." . $extension;
    $old_x          =   imageSX($src_img);
    $old_y          =   imageSY($src_img);

    // Calculate ratio of desired maximum sizes and original sizes.
    $widthRatio = $new_width / $old_x;
    $heightRatio = $new_height / $old_y;

    // Ratio used for calculating new image dimensions.
    $ratio = min($widthRatio, $heightRatio);

    // Calculate new image dimensions.
    $thumb_w  = (int)$old_x  * $ratio;
    $thumb_h = (int)$old_y * $ratio;

    // Create resized image
    $dst_img        =   ImageCreateTrueColor($thumb_w, $thumb_h);
    imagecopyresampled($dst_img, $src_img, 0, 0, 0, 0, $thumb_w, $thumb_h, $old_x, $old_y);

    /* Local storage system - VP - 12/08/2025 - Start */
    // New save location
    if($storage_system == 'local'){
        $new_thumb_loc = $moveToDir . $image_name;
        if ($mime['mime'] == 'image/png') {
            $result = @imagepng($dst_img, $new_thumb_loc, 8);
        }
        if ($mime['mime'] == 'image/jpg' || $mime['mime'] == 'image/jpeg' || $mime['mime'] == 'image/pjpeg') {
            $result = @imagejpeg($dst_img, $new_thumb_loc, 80);
        }
    }
    /* Local storage system - VP - 12/08/2025 - end */

    // Output to string buffer instead of file
    if($storage_system == 's3'){        
        ob_start();
        imagejpeg($dst_img, null, 80); // 80% quality
        $image_data = ob_get_clean();
    

        // Upload directly to S3
        $fileName = $image_name;        
        Storage::disk('s3')->put($fileName, $image_data); // Storage disk set to S3 in config/filesystems.php
        Storage::disk('s3')->setVisibility($fileName, 'public');
    }

    // Clean up
    imagedestroy($dst_img);
    imagedestroy($src_img);

    if($storage_system == 'local'){
        /* Local storage system - VP - 12/08/2025 - Start */
        if ($result == 1)
            return asset('storage/' . $uploaddir . '/' . $image_name);
        else
            return '';
        /* Local storage system - VP - 12/08/2025 - end */
    } elseif ($storage_system == 's3') {
        // Return S3 file URL
        return Storage::disk('s3')->url($fileName);
    }
}

function ImageValidaion($img)
{
    $myfile = fopen($img, "r") or die("Unable to open file!");

    $value = fread($myfile, filesize($img));

    if (strpos($value, "<?php") !== false)
        $img = 0;
    elseif (strpos($value, "<?=") !== false)
        $img = 0;
    elseif (strpos($value, "eval") !== false)
        $img = 0;
    elseif (strpos($value, "<script") !== false)
        $img = 0;
    else
        $img = 1;

    fclose($myfile);
    return $img;
}

function sendMail($thisEmail, $type, $thisMsg)
{
    try {
        Mail::to($thisEmail)->send(new UserMaill($thisEmail, $type, $thisMsg)); // UserMaill is the Mailable class
    } catch (\Exception $e) {
        \Log::info(print_r($e,true));
        dd($e);
    }
}

function getFavouriteTradePairs($tradepair_id)
{
    $user = Auth::guard('sanctum')->user(); // Use 'api' if using Passport
    if(!is_object($user)){
        return 0;
    }
    $fav = Favourite::where(['uid' => $user->id,'pair_id' => $tradepair_id])->first();
    return is_object($fav) ? 1 : 0;
}

function ProfileValidation($request)
    {
        $validator = Validator::make($request->all(), [
            'nickname' => 'required|regex:/^[\pL\s\-]+$/u|max:100|min:2',
            'bio'       => 'required|regex:/^[0-9a-zA-Z- _.,*\r\n]+$/|max:255',
            'phone_no'  => 'required|min:6|max:20',
            'birth_date' => 'required|after:-100 years|before:-18 years',
            'twitter_id'    => 'nullable|url|max:100|min:2',
            'telegram_id'   => 'nullable|url|max:100|min:2',
            'instagram_id'  => 'nullable|url|max:100|min:2',
            'website'       => 'nullable|url|max:100|min:2'
        ]);

        if ($validator->fails()) {
            return $this->sendError('', $validator->errors());
        }
    }
 
?>